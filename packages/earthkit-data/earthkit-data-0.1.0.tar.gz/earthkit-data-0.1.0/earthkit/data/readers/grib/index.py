# (C) Copyright 2022 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import json
import logging
import os
from abc import abstractmethod
from collections import namedtuple
from typing import List

from earthkit.data.core.caching import auxiliary_cache_file, cache_file
from earthkit.data.core.index import (
    Index,
    MaskIndex,
    MultiIndex,
    Order,
    OrderOrSelection,
    Selection,
    SelectionByIndex,
)
from earthkit.data.decorators import cached_method
from earthkit.data.indexing.database.json import JsonDatabase
from earthkit.data.indexing.database.sql import SqlDatabase
from earthkit.data.readers.grib.codes import GribField, get_messages_positions
from earthkit.data.readers.grib.fieldset import FieldSetMixin
from earthkit.data.utils import progress_bar
from earthkit.data.utils.parts import Part
from earthkit.data.utils.serialise import register_serialisation

LOG = logging.getLogger(__name__)


class FieldSet(FieldSetMixin, Index):
    _availability = None

    def __init__(self, *args, **kwargs):

        Index.__init__(self, *args, **kwargs)

    @classmethod
    def new_mask_index(self, *args, **kwargs):
        return MaskFieldSet(*args, **kwargs)

    @property
    def availability(self):
        raise NotImplementedError()
        if self._availability is not None:
            return self._availability.tree()
        LOG.debug("Building availability")

        def dicts():
            for i in self:
                dic = i.to_dict()  # GribField.to_dict() is not implemented
                i = {k: v for k, v in dic.items() if not k.startswith("_")}
                yield i

        from earthkit.data.utils.availability import Availability

        self._availability = Availability(dicts())
        return self.availability


class MaskFieldSet(FieldSet, MaskIndex):
    def __init__(self, *args, **kwargs):
        MaskIndex.__init__(self, *args, **kwargs)


class MultiFieldSet(FieldSet, MultiIndex):
    def __init__(self, *args, **kwargs):
        MultiIndex.__init__(self, *args, **kwargs)


class FieldSetInFiles(FieldSet):
    # Remote Fieldsets (with urls) are also here,
    # as the actual fieldset is accessed on a file in cache.
    # This class changes the interface (_getitem__ and __len__)
    # into the interface (part and number_of_parts).
    def __getitem__(self, n):
        if isinstance(n, int):
            part = self.part(n if n >= 0 else len(self) + n)
            return GribField(part.path, part.offset, part.length)
        else:
            return self.subindex(n)

    def __len__(self):
        return self.number_of_parts()

    @abstractmethod
    def part(self, n):
        self._not_implemented()

    @abstractmethod
    def number_of_parts(self):
        self._not_implemented()


class FieldsetInFilesWithDBIndex(FieldSetInFiles):
    def __init__(self, db, **kwargs):
        """Should not be instantiated directly.
        The public API are the constructors "_from*()" class methods.
        """
        self.db = db

        # self._cache is a tuple : (first, length, result). It holds one chunk of the db.
        # The third element (result) is a list of size length.
        self._cache = None
        self._dict_cache = None

        super().__init__(**kwargs)

    @classmethod
    def from_iterator(
        cls,
        iterator,
        cache_metadata,
        selection=None,
        order_by=None,
        **kwargs,
    ):
        def load(target, *args):
            LOG.debug(f"Building db in {target}")
            db = cls.DBCLASS(target)
            db.load(iterator)

        db_name = cache_file(
            "grib-index",
            load,
            cache_metadata,
            hash_extra=cls.DBCLASS.VERSION,
            extension=cls.DBCLASS.EXTENSION,
        )

        db = cls.DBCLASS(db_name)

        new = cls(db=db, **kwargs)
        new = new.sel(selection)
        new = new.order_by(order_by)
        return new

    @classmethod
    def from_file(cls, path, **kwargs):
        directory = os.path.dirname(path)
        size = os.path.getsize(path)

        def progress(lines):
            pbar = progress_bar(iterable=lines, desc="Parsing index", total=size)
            for line in pbar:
                yield line
                pbar.update(len(line) + 1)

        def parse_lines(lines):
            for line in lines:
                entry = json.loads(line)
                if not os.path.isabs(entry["_path"]):
                    entry["_path"] = os.path.join(directory, entry["_path"])
                yield entry

        iterator = open(path)
        iterator = progress(iterator)
        iterator = parse_lines(iterator)

        return cls.from_iterator(
            iterator=iterator,
            cache_metadata={"path": path},
            **kwargs,
        )

    @classmethod
    def from_existing_db(cls, db_path, **kwargs):
        assert os.path.exists(db_path)
        return cls(cls.DBCLASS(db_path), **kwargs)

    @property
    def availability(self):
        if self._availability is not None:
            return self._availability.tree()

        LOG.debug("Building availability")

        def dicts():
            for i in self.db.lookup_dicts(keys="i"):
                dic = {}
                for k, v in i.items():
                    if k.startswith("i_"):
                        k = k[2:]
                    dic[k] = v
                yield dic

        from earthkit.data.utils.availability import Availability

        self._availability = Availability(dicts())
        return self.availability


class FieldsetInFilesWithJsonIndex(FieldsetInFilesWithDBIndex):
    DBCLASS = JsonDatabase

    @cached_method
    def _lookup_parts(self):
        return self.db.lookup_parts()

    def part(self, n):
        return self._lookup_parts()[n]

    def number_of_parts(self):
        return len(self._lookup_parts())


SqlResultCache = namedtuple("SqlResultCache", ["first", "length", "result"])


class FieldsetInFilesWithSqlIndex(FieldsetInFilesWithDBIndex):

    DBCLASS = SqlDatabase
    DB_CACHE_SIZE = 50_000
    DB_DICT_CACHE_SIZE = 5_000

    def __init__(self, *args, **kwargs):
        """
        _filters are used to keep the state of the db
        It is a list of **already applied** filters, not a list of filter to apply.
        Use the method apply_filters for this.
        """
        super().__init__(*args, **kwargs)

    def apply_filters(self, filters: List[OrderOrSelection]):
        obj = self
        for f in filters:
            obj = obj.filter(f)
        return obj

    def _find_coords_keys(self):
        return self.db._find_coords_keys()

    def _find_coord_values(self, key):
        return self.db._find_coord_values(key)

    def filter(self, filter):
        if filter.is_empty:
            return self

        db = self.db.filter(filter)
        return self.__class__(db=db)

    def sel(self, *args, **kwargs):
        s = Selection(*args, **kwargs)
        for k in s.selection:
            if not self.db.has_column(k):
                raise KeyError(f"sel: GRIB key={k} not found in index db")

        return self.filter(s)

    def isel(self, *args, **kwargs):
        s = SelectionByIndex(None, *args, **kwargs)
        for k in s.selection:
            if not self.db.has_column(k):
                raise KeyError(f"isel: GRIB key={k} not found in index db")

        return self.filter(SelectionByIndex(self.coord, *args, **kwargs))

    def order_by(self, *args, **kwargs):
        order = Order(*args, **kwargs)
        for k in order.order:
            if not self.db.has_column(k):
                raise KeyError(f"order_by: GRIB key={k} not found in index db")

        return self.filter(Order(*args, **kwargs))

    def part(self, n):
        if self._cache is None or not (
            self._cache.first <= n < self._cache.first + self._cache.length
        ):
            first = n // self.DB_CACHE_SIZE
            result = self.db.lookup_parts(limit=self.DB_CACHE_SIZE, offset=first)
            self._cache = SqlResultCache(first, len(result), result)
        return self._cache.result[n % self.DB_CACHE_SIZE]

    def get_metadata(self, n):
        if self._dict_cache is None or not (
            self._dict_cache.first
            <= n
            < self._dict_cache.first + self._dict_cache.length
        ):
            first = n // self.DB_DICT_CACHE_SIZE
            result = self.db.lookup_dicts(
                limit=self.DB_DICT_CACHE_SIZE, offset=first, keys=["i", "c"]
            )

            self._dict_cache = SqlResultCache(first, len(result), result)
        return self._dict_cache.result[n % self.DB_DICT_CACHE_SIZE]

    @cached_method
    def number_of_parts(self):
        return self.db.count()

    @classmethod
    def merge(cls, readers):

        assert all(isinstance(s, FieldsetInFilesWithSqlIndex) for s in readers), readers
        assert len(readers) > 1

        return MultiFieldSet(readers)


register_serialisation(
    FieldsetInFilesWithSqlIndex,
    lambda x: [x.db.db_path, x.db._filters],
    lambda x: FieldsetInFilesWithSqlIndex(db=SqlDatabase(x[0])).apply_filters(
        filters=x[1]
    ),
)


class FieldSetInOneFile(FieldSetInFiles):
    VERSION = 1

    def __init__(self, path, **kwargs):
        assert isinstance(path, str), path

        self.path = path
        self.offsets = None
        self.lengths = None
        self.mappings_cache_file = auxiliary_cache_file(
            "grib-index",
            path,
            content="null",
            extension=".json",
        )

        if not self._load_cache():
            self._build_offsets_lengths_mapping()

        super().__init__(**kwargs)

    def _build_offsets_lengths_mapping(self):

        offsets = []
        lengths = []

        for offset, length in get_messages_positions(self.path):
            offsets.append(offset)
            lengths.append(length)

        self.offsets = offsets
        self.lengths = lengths

        self._save_cache()

    def _save_cache(self):
        try:
            with open(self.mappings_cache_file, "w") as f:
                json.dump(
                    dict(
                        version=self.VERSION,
                        offsets=self.offsets,
                        lengths=self.lengths,
                    ),
                    f,
                )
        except Exception:
            LOG.exception("Write to cache failed %s", self.mappings_cache_file)

    def _load_cache(self):
        try:
            with open(self.mappings_cache_file) as f:
                c = json.load(f)
                if not isinstance(c, dict):
                    return False

                assert c["version"] == self.VERSION
                self.offsets = c["offsets"]
                self.lengths = c["lengths"]
                return True
        except Exception:
            LOG.exception("Load from cache failed %s", self.mappings_cache_file)

        return False

    def part(self, n):
        return Part(self.path, self.offsets[n], self.lengths[n])

    def number_of_parts(self):
        return len(self.offsets)
