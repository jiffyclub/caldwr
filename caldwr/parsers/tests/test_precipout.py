import pandas as pd
import pytest

from caldwr.parsers import precipout


@pytest.fixture(scope='module')
def url():
    return 'http://cdec.water.ca.gov/cgi-progs/reports/PRECIPOUT'


def test_load_precipout(url):
    data = precipout.load_precipout(url)
    assert isinstance(data, pd.DataFrame)


def test_load_precipout_year(url):
    year = 2015
    data = precipout.load_precipout(url, year=year)
    assert isinstance(data, pd.DataFrame)
    assert 'year' in data
    assert data['year'].iloc[0] == year
