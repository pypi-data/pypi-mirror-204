#!/usr/bin/env python3

# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import os
import shutil
import warnings

import earthkit.data
from earthkit.data.core.temporary import temp_directory, temp_file
from earthkit.data.readers.grib.index import FieldSet
from earthkit.data.testing import (
    earthkit_examples_file,
    earthkit_file,
    earthkit_test_data_file,
)

TEST_GRIB_FILES = [
    earthkit_file(p)
    for p in [
        "docs/examples/test.grib",
        "docs/examples/test4.grib",
    ]
]


def dir_with_grib_files():
    tmp = temp_directory()
    _build_dir_with_grib_files(tmp.path)
    return tmp


def _build_dir_with_grib_files(testdir):
    os.makedirs(testdir, exist_ok=True)
    for p in ["t", "u", "v"]:
        shutil.copy(earthkit_test_data_file(f"{p}_pl.grib"), testdir)


def unique_grib_file():
    tmp = temp_file()
    _build_unique_grib_file(tmp.path)
    return tmp


def unique_grib_file_list():
    tmp = temp_file()
    _build_unique_grib_file(tmp.path, name="test.grib")
    tmp1 = temp_file()
    _build_unique_grib_file(tmp1.path, name="test4.grib")
    return [tmp, tmp1]


def _build_unique_grib_file(path, name="tuv_pl.grib"):
    shutil.copy(earthkit_examples_file(name), path)


def list_of_dicts():
    prototype = {
        "gridType": "regular_ll",
        "Nx": 2,
        "Ny": 3,
        "distinctLatitudes": [-10.0, 0.0, 10.0],
        "distinctLongitudes": [0.0, 10.0],
        "_param_id": 167,
        "values": [[1, 2], [3, 4], [5, 6]],
        "date": "20180801",
        "time": "1200",
    }
    return [
        {"param": "t", "levelist": 500, **prototype},
        {"param": "t", "levelist": 850, **prototype},
        {"param": "u", "levelist": 500, **prototype},
        {"param": "u", "levelist": 850, **prototype},
        {"param": "d", "levelist": 850, **prototype},
        {"param": "d", "levelist": 600, **prototype},
    ]


class GribIndexFromDicts(FieldSet):
    def __init__(self, list_of_dicts, *args, **kwargs):
        self.list_of_dicts = list_of_dicts
        super().__init__(*args, **kwargs)

    def __getitem__(self, n):
        class _VirtualGribField(dict):
            def metadata(_self, n):
                try:
                    if n == "level":
                        n = "levelist"
                    if n == "shortName":
                        n = "param"
                    if n == "paramId":
                        n = "_param_id"
                    return _self[n]
                except KeyError:
                    warnings.warn("Cannot find all metadata keys.")

            @property
            def values(self, n):
                return self["values"]

        return _VirtualGribField(self.list_of_dicts[n])

    def __len__(self):
        return len(self.list_of_dicts)


def get_fixtures_directory(indexing, request):
    tmp = dir_with_grib_files()
    total, n = 18, 4
    ds = earthkit.data.from_source("file", tmp.path, indexing=indexing, **request)
    return ds, tmp, total, n


def get_fixtures_file(indexing, request):
    tmp = unique_grib_file()
    total, n = 18, 4
    ds = earthkit.data.from_source("file", tmp.path, indexing=indexing, **request)
    return ds, tmp, total, n


def get_fixtures_list_of_dicts(indexing, request):
    tmp = list_of_dicts()
    total, n = 6, 4
    ds = GribIndexFromDicts(tmp, **request)
    ds = ds.mutate()
    return ds, tmp, total, n


def get_fixtures(input_mode, indexing, *args, **kwargs):
    return {
        "directory": get_fixtures_directory,
        "file": get_fixtures_file,
        "list-of-dicts": get_fixtures_list_of_dicts,
        # "indexed-url": get_fixtures_indexed_url,
        # "indexed-urls": get_fixtures_indexed_urls,
    }[input_mode](indexing, *args, **kwargs)


def check_sel_and_order(ds, params, levels):
    assert ds[0].metadata("param") == params[0]
    assert ds[1].metadata("param") == params[1]
    assert ds[2].metadata("param") == params[0]
    assert ds[3].metadata("param") == params[1]

    assert ds[0].metadata("level") == levels[0]
    assert ds[1].metadata("level") == levels[0]
    assert ds[2].metadata("level") == levels[1]
    assert ds[3].metadata("level") == levels[1]
