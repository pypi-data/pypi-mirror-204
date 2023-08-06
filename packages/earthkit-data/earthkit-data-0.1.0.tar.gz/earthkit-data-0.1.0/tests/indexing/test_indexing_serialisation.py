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
import sys

import pytest

from earthkit.data.utils.serialise import (
    SERIALISATION,
    deserialise_state,
    serialise_state,
)

here = os.path.dirname(__file__)
sys.path.insert(0, here)
from indexing_fixtures import check_sel_and_order, get_fixtures  # noqa: E402


@pytest.mark.parametrize("params", (["t", "u"], ["u", "t"]))
@pytest.mark.parametrize("levels", ([500, 850], [850, 500]))
@pytest.mark.parametrize(
    "input_mode",
    [
        "directory",
        # "list-of-dicts",
        # "file",
    ],
)
@pytest.mark.parametrize("indexing", [True])
def test_indexing_pickle(params, levels, input_mode, indexing):
    request = dict(
        level=levels,
        variable=params,
        date=20180801,
        time="1200",
    )

    ds, __tmp, total, n = get_fixtures(input_mode, indexing, {})
    assert len(ds) == total, len(ds)

    ds = ds.sel(**request)
    ds = ds.order_by(level=levels, variable=params)

    assert len(ds) == n, (len(ds), ds, SERIALISATION)
    state = serialise_state(ds)
    ds = deserialise_state(state)
    assert len(ds) == n, (len(ds), ds, SERIALISATION)

    check_sel_and_order(ds, params, levels)


if __name__ == "__main__":
    from earthkit.data.testing import main

    main(__file__)
