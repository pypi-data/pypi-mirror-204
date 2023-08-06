# (C) Copyright 2021 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#


import logging
import os
import sqlite3
from collections import namedtuple
from threading import local

import earthkit.data
from earthkit.data.core.index import Order, OrderOrSelection, Selection
from earthkit.data.utils import tqdm
from earthkit.data.utils.parts import Part

from . import Database

LOG = logging.getLogger(__name__)


GribKey = namedtuple("GribKey", ["name", "type", "type_in_db", "default_order"])

GRIB_INDEX_KEYS_DICT = {}
GRIB_INDEX_KEYS = []
for k in [
    GribKey("class", str, str, None),
    GribKey("stream", str, str, None),
    GribKey("levtype", str, str, None),
    GribKey("type", str, str, None),
    GribKey("expver", str, str, None),
    GribKey("date", str, str, None),
    GribKey("hdate", str, str, None),
    GribKey("andate", str, str, None),
    GribKey("time", str, str, None),
    GribKey("antime", str, str, None),
    GribKey("reference", str, str, None),
    GribKey("step", str, str, None),
    GribKey("anoffset", str, str, None),
    GribKey("verify", str, str, None),
    GribKey("fcmonth", str, str, None),
    GribKey("fcperiod", str, str, None),
    GribKey("leadtime", str, str, None),
    GribKey("opttime", str, str, None),
    GribKey("origin", str, str, None),
    GribKey("domain", str, str, None),
    GribKey("method", str, str, None),
    GribKey("diagnostic", str, str, None),
    GribKey("iteration", str, str, None),
    GribKey("number", str, str, None),
    GribKey("quantile", str, str, None),
    GribKey("levelist", str, str, None),
    # "latitude"  # in the MARS vocabulary but not used.
    # "longitude"  # in the MARS vocabulary but not used.
    GribKey("range", str, str, None),
    GribKey("param", str, str, None),
    GribKey("ident", str, str, None),
    GribKey("obstype", str, str, None),
    GribKey("instrument", str, str, None),
    GribKey("reportype", str, str, None),
    GribKey("frequency", str, str, None),  # for 2-d wave-spectra products
    GribKey("direction", str, str, None),  # for 2-d wave-spectra products
    GribKey("channel", str, str, None),  # for ea and ef
]:
    GRIB_INDEX_KEYS_DICT[k.name] = k
    GRIB_INDEX_KEYS.append(k.name)
STATISTICS_KEYS = ["mean", "std", "min", "max"]
CFGRIB_KEYS = ["md5_grid_section"]


class SqlSorter:
    @property
    def _func_name(self):
        return f"userorder_{self.view}"

    def __init__(self, order, view):
        self.order = order
        self.view = view

        self.dict_of_dicts = dict()
        self.order_lst = []

        # TODO: To improve speed, we could use ASC or DESC when lst is already sorted
        # TODO: move GRIB_INDEX_KEYS and two comments above to upper class
        # Use mars keys order by default
        # But make sure the order provided by the user
        # in the order override this default order.

        if order is None or order.is_empty:
            return

        for key, lst in self.order.items():
            self._add_key(key, lst)

    def _add_key(self, key, lst):
        if lst is None:
            self.order_lst.append(f"i_{key}")
            return
        if lst == "ascending":
            self.order_lst.append(f"i_{key} ASC")
            return
        if lst == "descending":
            self.order_lst.append(f"i_{key} DESC")
            return
        if not isinstance(lst, (list, tuple)):
            lst = [lst]

        lst = [str(_) for _ in lst]  # processing only strings from now.

        self.dict_of_dicts[key] = dict(zip(lst, range(len(lst))))
        self.order_lst.append(f'{self._func_name}("{key}",i_{key})')

    @property
    def order_statement(self):
        if not self.order_lst:
            assert not self.dict_of_dicts, self.dict_of_dicts
            return ""
        return "ORDER BY " + ",".join(self.order_lst)

    def create_sql_function_if_needed(self, connection):
        if not self.dict_of_dicts:
            return

        dict_of_dicts = self.dict_of_dicts  # avoid creating closure on self.

        def order_func(k, v):
            return dict_of_dicts[k][v]

        connection.create_function(self._func_name, 2, order_func)


class Connection(local):
    # Inheriting from threading.local allows one connection for each thread
    # __init__ is "called each time the local object is used in a separate thread".
    # https://github.com/python/cpython/blob/0346eddbe933b5f1f56151bdebf5bd49392bc275/Lib/_threading_local.py#L65
    def __init__(self, db_path):
        self._conn = sqlite3.connect(db_path)


class SqlDatabase(Database):
    VERSION = 3
    EXTENSION = ".db"

    def __init__(
        self,
        db_path,
        filters=None,
    ):
        self._cache_column_names = {}

        self.db_path = db_path
        self._filters = filters or []
        self._view = None
        self._connection = None

    @property
    def view(self):
        if self._view is None:
            self._view = "entries"
            for f in self._filters:
                self._apply_filter(f)
            LOG.debug("DB %s %s", self.db_path, self.view)
        return self._view

    @property
    def connection(self):
        if self._connection is None:
            self._connection = Connection(self.db_path)
        return self._connection._conn

    def _apply_filter(self, filter: OrderOrSelection):
        # This method updates self.view with the additional filter

        old_view = self._view
        new_view = old_view + "_" + filter.h(parent_view=old_view)

        if isinstance(filter, Selection):
            order = None
            selection = filter
        elif isinstance(filter, Order):
            selection = None
            order = filter
        else:
            assert False, (type(filter), filter)

        conditions_statement = self._conditions(selection)
        sorter = SqlSorter(order, new_view)
        statement = (
            f"CREATE TEMP VIEW IF NOT EXISTS {new_view} AS SELECT * "
            + f"FROM {old_view} {conditions_statement} {sorter.order_statement};"
        )

        sorter.create_sql_function_if_needed(self.connection)
        LOG.debug("%s", statement)
        for i in self.connection.execute(statement):
            LOG.error(str(i))  # Output of .execute should be empty

        self._view = new_view

    def filter(self, filter: OrderOrSelection):
        return self.__class__(
            self.db_path,
            filters=self._filters + [filter],
        )

    def load(self, iterator):
        with self.connection as conn:

            # The i_ is to avoid clashes with SQL keywords
            i_columns = [f"i_{n}" for n in GRIB_INDEX_KEYS]
            s_columns = [f"s_{n}" for n in STATISTICS_KEYS]
            c_columns = [f"c_{n}" for n in CFGRIB_KEYS]
            columns = i_columns + s_columns + c_columns

            i_columns_defs = ",".join([f"{c} TEXT" for c in i_columns])
            s_columns_defs = ",".join([f"{c} FLOAT" for c in s_columns])
            c_columns_defs = ",".join([f"{c} TEXT" for c in c_columns])
            create_statement = f"""CREATE TABLE IF NOT EXISTS entries (
                path    TEXT,
                offset  INTEGER,
                length  INTEGER,
                {i_columns_defs},
                {s_columns_defs},
                {c_columns_defs}
                );"""
            LOG.debug("%s", create_statement)
            conn.execute(create_statement)

            names = ",".join(columns)
            values = ",".join(["?"] * (3 + len(columns)))
            insert_statement = f"""
                INSERT INTO entries (path, offset, length, {names})
                VALUES({values});
                """
            LOG.debug("%s", insert_statement)

            # insert each entry
            count = 0
            for entry in iterator:
                assert isinstance(entry, dict), (type(entry), entry)
                values = [entry["_path"], entry["_offset"], entry["_length"]] + [
                    entry.get(n)
                    for n in GRIB_INDEX_KEYS + STATISTICS_KEYS + CFGRIB_KEYS
                ]
                conn.execute(insert_statement, tuple(values))
                count += 1

            assert count >= 1, "No entry found."
            LOG.info("Added %d entries", count)

            pbar = tqdm(i_columns + ["path"], desc="Building indexes")
            for n in pbar:
                pbar.set_description(f"Building index for {n}")
                conn.execute(f"CREATE INDEX IF NOT EXISTS {n}_index ON entries ({n});")

            return count

    def _conditions(self, selection):
        if selection is None or selection.is_empty:
            return ""
        conditions = []
        for k, b in selection.dic.items():
            if b is None or b == earthkit.data.ALL:
                continue
            elif isinstance(b, (list, tuple)):
                if len(b) == 1:
                    conditions.append(f"i_{k}='{b[0]}'")
                    continue
                w = ",".join([f"'{x}'" for x in b])
                conditions.append(f"i_{k} IN ({w})")
            else:
                conditions.append(f"i_{k}='{b}'")

        if not conditions:
            return ""
        return " WHERE " + " AND ".join(conditions)

    def has_column(self, name):
        for prefix in ("i", "s", "c"):
            if name in self._columns_names(prefix, True):
                return True
        return False

    def _columns_names(self, prefix, remove_prefix):
        if prefix in self._cache_column_names:
            return self._cache_column_names[(prefix, remove_prefix)]

        assert len(prefix) == 1, prefix
        cursor = self.connection.execute("PRAGMA table_info(entries)")
        out = []
        for x in cursor.fetchall():
            name = x[1]
            if not name.startswith(prefix):
                continue
            if remove_prefix:
                name = name[2:]
            out.append(name)

        self._cache_column_names[(prefix, remove_prefix)] = out
        return out

    def lookup_parts(self, limit=None, offset=None, resolve_paths=True):
        """
        Look into the database and provide entries as Parts.
        limit: Returns only "limit" entries (used for paging).
        offset: Skip the first "offset" entries (used for paging).
        """
        _names = ["path", "offset", "length"]
        parts = []
        for path, offset, length in self._execute_select(_names, limit, offset):
            parts.append(Part(path, offset, length))
        if resolve_paths:
            parts = Part.resolve(parts, os.path.dirname(self.db_path))
        return parts

    def lookup_dicts(self, keys=None, limit=None, offset=None):
        """
        From a list of keys, return dicts with these columns of the database.
        limit: Returns only "limit" entries (used for paging).
        offset: Skip the first "offset" entries (used for paging).
        """
        if not isinstance(keys, (list, tuple)):
            keys = [keys]

        _names = []
        for k in keys:
            assert k in ["i", "s", "c"], k
            _names += self._columns_names(k, remove_prefix=False)

        def remove_prefix(k):
            for prefix in ["i", "s", "c"]:
                if k.startswith(prefix + "_"):
                    return k[2:]
            return k

        dicts = []
        for tupl in self._execute_select(_names, limit, offset):
            dic = {remove_prefix(k): v for k, v in zip(_names, tupl)}
            dicts.append(dic)
        return dicts

    def _execute_select(self, names, limit, offset):
        names_str = ",".join([x for x in names]) if names else "*"
        limit_str = f" LIMIT {limit}" if limit is not None else ""
        offset_str = f" OFFSET {offset}" if offset is not None else ""

        statement = f"SELECT {names_str} FROM {self.view} {limit_str} {offset_str};"
        LOG.debug("%s", statement)

        for tupl in self.connection.execute(statement):
            yield tupl

    def _find_coords_keys(self):
        keys = GRIB_INDEX_KEYS  # default keys ordering
        for f in self._filters:
            new = list(f.keys())
            keys = new + [k for k in keys if k not in new]
        return keys

    def _find_coord_values(self, key):
        def get_order():
            orders = [f for f in self._filters if isinstance(f, Order)]
            if not orders:
                return None

            order = Order()
            for other in reversed(orders):
                order.update(other)
            return order

        order = get_order()

        order_statement = ""
        if order:
            sorter = SqlSorter(order, self.view)
            order_statement = sorter.order_statement
            sorter.create_sql_function_if_needed(self.connection)

        statement = f"SELECT DISTINCT i_{key} FROM {self.view} {order_statement};"
        lst = []
        for result in self.connection.execute(statement):
            value = result[0]
            lst.append(value)
        return lst

    def count(self):
        statement = f"SELECT COUNT(*) FROM {self.view};"
        for result in self.connection.execute(statement):
            return result[0]
        assert False, statement  # Fail if result is empty.

    def _dump_dicts(self):
        # TODO: duplicated code here and in lookup_dict
        names, x_names = [], []

        names += ["_path", "_offset", "_length"]
        x_names += ["path", "offset", "length"]

        for prefix in ["i", "s", "c"]:
            names += self._columns_names(prefix, remove_prefix=True)
            x_names += self._columns_names(prefix, remove_prefix=False)

        s = ",".join(x_names)
        statement = f"SELECT {s} FROM entries ;"
        for tupl in self.connection.execute(statement):
            yield {k: v for k, v in zip(names, tupl)}

    def dump_dicts(self, remove_none=True):
        for dic in self._dump_dicts():
            if remove_none:
                dic = {k: v for k, v in dic.items() if v is not None}
            yield dic

    def duplicate_db(self, filename, **kwargs):
        new = SqlDatabase(db_path=filename)
        new.load(self.dump_dicts(**kwargs))
