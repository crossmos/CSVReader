import pytest
import csv
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from main import CSVProcessor

TEST_CSV = 'test_data.csv'
TEST_CONTENT = [
    ['name', 'brand', 'price', 'rating'],
    ['iphone 15 pro', 'apple', '999', '4.9'],
    ['galaxy s23 ultra', 'samsung', '1199', '4.8'],
    ['redmi note 12', 'xiaomi', '199', '4.6'],
    ['poco x5 pro', 'xiaomi', '299', '4.4']
]

@pytest.fixture(scope='module')
def test_csv_file(tmp_path_factory):
    file = tmp_path_factory.mktemp('data') / TEST_CSV
    with open(file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(TEST_CONTENT)
    return str(file)

@pytest.fixture(scope='module')
def processor(test_csv_file):
    return CSVProcessor(test_csv_file) 