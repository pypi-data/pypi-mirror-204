#!/usr/bin/python3

import pytest
from nx5d.xrd import kmc3 as kmc3

@pytest.fixture
def testfile():

    # Note that, for data storage reasons within the git project,
    # our testfile contains only TIFF data for scan "2.1".
    return "./tests/test_data/spech5/231-cw7-12083-roessle.spec"


def test_spectiff(testfile):

    h5like = kmc3.SpecTiffH5(testfile)

    assert "2.1" in h5like
    assert "44.1" in h5like ## scan is available, but no tiff data

    scan = h5like["2.1"]

    for i in [ "measurement", "instrument" ]:
        assert i in scan

    assert "pilatus" in scan["measurement"]
    assert "data" in scan["instrument/pilatus"]

    d1 = scan['measurement/pilatus']
    d2 = scan['instrument/pilatus/data']

    for i,j in zip(d1.shape, d2.shape):
        assert i == j
        assert j != 0

    # There's only one image in scan "2.1"
    assert len(d1) == 1

    assert (d1 == d2).all()
    
