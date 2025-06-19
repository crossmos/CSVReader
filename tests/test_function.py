import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from main import CSVProcessor


def test_read_csv(test_csv_file, processor):
    assert processor.file == test_csv_file
    assert len(processor.data) == 5
    assert processor.headers == ['name', 'brand', 'price', 'rating']

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        CSVProcessor('no_such_file.csv')

def test_empty_file(tmp_path):
    empty = tmp_path / 'empty.csv'
    empty.write_text('')
    with pytest.raises(ValueError):
        CSVProcessor(str(empty))

@pytest.mark.parametrize(
    "condition,expected_len,expected_first_string",
    [
        ("brand=apple", 2, "iphone 15 pro"),
        ("brand>apple", 4, "galaxy s23 ultra"),
        ("brand<samsung", 2, "iphone 15 pro"),
        ("price=999", 2, "iphone 15 pro"),
        ("price>1000", 2, "galaxy s23 ultra"),
        ("price<1200", 5, "iphone 15 pro"),
        ("rating=4.4", 2, "poco x5 pro"),
        ("rating>4.8", 2, "iphone 15 pro"),
        ("rating<4.7", 3, "redmi note 12"),
    ]
)
def test_filter_success(processor, condition, expected_len, expected_first_string):
    filtered_data = processor.filter_data(condition, processor.data)
    assert len(filtered_data) == expected_len
    assert filtered_data[1][0] == expected_first_string


@pytest.mark.parametrize(
    "condition,expected_result",
    [
        ("price=avg", (999+1199+199+299)/4),
        ("price=max", 1199),
        ("price=min", 199),
        ("rating=avg", (4.9+4.8+4.6+4.4)/4),
        ("rating=max", 4.9),
        ("rating=min", 4.4),
    ]
)
def test_aggregate_success(processor, condition, expected_result):
    result = processor.aggregate_data(condition, processor.data)
    assert abs(result[1][0] - expected_result) < 1e-6

@pytest.mark.parametrize(
    "condition,error_message",
    [
        ("type=apple", "Столбец 'type' не найден в данных"),
        ("brand.apple", r"Неподдерживаемое условие фильтрации\. Используйте одно из: \['>',\s'<',\s'='\]"),
        ("brand=nonexistent", "Нет данных подходящих под условия фильтра"),
    ]
)
def test_filter_errors(processor, condition, error_message):
    with pytest.raises(ValueError, match=error_message):
        processor.filter_data(condition, processor.data)


@pytest.mark.parametrize(
    "condition,error_message",
    [
        ("screen_size=max", "Столбец 'screen_size' не найден в данных"),
        ("price=sum", r"Неподдерживаемое условие агрегации: sum. Используйте одно из: \['avg',\s'min',\s'max'\]"),
        ("price>min", "Формат условия должен быть header=action, например rating=avg"),
        ("brand=avg", "Столбец 'brand' содержит нечисловые значения"),
    ]
)
def test_aggregate_errors(processor, condition, error_message):
    with pytest.raises(ValueError, match=error_message):
        processor.aggregate_data(condition, processor.data)
