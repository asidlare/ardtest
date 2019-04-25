import pytest
from unittest.mock import patch
from models.valuation_service import valuate, tmpdir
from open_file_mock import MockOpen
import os
import io


currencies = """currency,ration
GBP,2.4
EU,2.1
PLN,1
"""

data = """id,price,currency,quantity,matching_id
1,1000,GBP,2,3
2,1050,EU,1,1
3,2000,PLN,1,1
4,1750,EU,2,2
5,1400,EU,4,3
6,7000,PLN,3,2
7,630,GBP,5,3
8,4000,EU,1,3
9,1400,GBP,3,1
"""

output = {
    'case_000': [['1', 0, 0, 'PLN', 3], ['2', 0, 0, 'PLN', 2], ['3', 0, 0, 'PLN', 4]],
    'case_223': [['1', 12285.0, 6142.5, 'PLN', 1], ['2', 28350.0, 14175.0, 'PLN', 0], ['3', 27720.0, 9240.0, 'PLN', 1]],
    'case_324': [['1', 14285.0, 4761.67, 'PLN', 0], ['2', 28350.0, 14175.0, 'PLN', 0], ['3', 32520.0, 8130.0, 'PLN', 0]],
    'case_555': [['1', 14285.0, 4761.67, 'PLN', 0], ['2', 28350.0, 14175.0, 'PLN', 0], ['3', 32520.0, 8130.0, 'PLN', 0]],
}


@pytest.fixture(scope='function')
def case_000():

    with patch('builtins.open', new_callable=MockOpen) as open_mock:
        open_mock.register_object_for_path(path=os.path.join(tmpdir, 'currencies.csv'), obj=io.StringIO(currencies))
        open_mock.register_object_for_path(path=os.path.join(tmpdir, 'data.csv'), obj=io.StringIO(data))
        open_mock.register_object_for_path(path=os.path.join(tmpdir, 'matchings.csv'),
                                           obj=io.StringIO("matching_id,top_priced_count\n1,0\n2,0\n3,0\n"))
        yield


@pytest.fixture(scope='function')
def case_223():

    with patch('builtins.open', new_callable=MockOpen) as open_mock:
        open_mock.register_object_for_path(path=os.path.join(tmpdir, 'currencies.csv'), obj=io.StringIO(currencies))
        open_mock.register_object_for_path(path=os.path.join(tmpdir, 'data.csv'), obj=io.StringIO(data))
        open_mock.register_object_for_path(path=os.path.join(tmpdir, 'matchings.csv'),
                                           obj=io.StringIO("matching_id,top_priced_count\n1,2\n2,2\n3,3\n"))
        yield


@pytest.fixture(scope='function')
def case_324():

    with patch('builtins.open', new_callable=MockOpen) as open_mock:
        open_mock.register_object_for_path(path=os.path.join(tmpdir, 'currencies.csv'), obj=io.StringIO(currencies))
        open_mock.register_object_for_path(path=os.path.join(tmpdir, 'data.csv'), obj=io.StringIO(data))
        open_mock.register_object_for_path(path=os.path.join(tmpdir, 'matchings.csv'),
                                           obj=io.StringIO("matching_id,top_priced_count\n1,3\n2,2\n3,4\n"))
        yield


@pytest.fixture(scope='function')
def case_555():

    with patch('builtins.open', new_callable=MockOpen) as open_mock:
        open_mock.register_object_for_path(path=os.path.join(tmpdir, 'currencies.csv'), obj=io.StringIO(currencies))
        open_mock.register_object_for_path(path=os.path.join(tmpdir, 'data.csv'), obj=io.StringIO(data))
        open_mock.register_object_for_path(path=os.path.join(tmpdir, 'matchings.csv'),
                                           obj=io.StringIO("matching_id,top_priced_count\n1,5\n2,5\n3,5\n"))
        yield


@pytest.mark.parametrize('case', ['case_000', 'case_223', 'case_324', 'case_555'])
def test_valuate(request, case):
    request.getfixturevalue(case)
    assert valuate() == output[case]
