import argparse
import csv
from pathlib import Path
from tabulate import tabulate


class CSVProcessor:
    def __init__(self, file: str):
        self.file = file
        self.data = self._read_csv()
        self.headers = self.data[0] if self.data else []

    def _read_csv(self) -> list[list[str]]:
        file_path = Path(self.file).expanduser().resolve()
        if not file_path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        with file_path.open('r', encoding='utf-8') as file:
            data = list(csv.reader(file))

        # Проверяю наличие данных при создании объекта,
        # чтобы сразу закончить выполнение функции, если их нет
        if not data:
            raise ValueError("Не переданы данные для обработки")
        return data


    def filter_data(self, condition: str, data: list[list[str]]) -> list[list[str]]:
        actions = {
            '>': lambda x, y: float(x) > float(y) if x.replace('.', '', 1).isdigit() and y.replace('.', '', 1).isdigit() else x > y,
            '<': lambda x, y: float(x) < float(y) if x.replace('.', '', 1).isdigit() and y.replace('.', '', 1).isdigit() else x < y,
            '=': lambda x, y: x == y
        }

        # Ищу есть ли в переданной строке доступное действие
        ordered_action = None
        for action in actions.keys():
            if action in condition:
                ordered_action = action
                break
        if not ordered_action:
            raise ValueError(f"Неподдерживаемое условие фильтрации. Используйте одно из: {list(actions.keys())}")

        # Разделяю переданную строку
        header, value = condition.split(ordered_action, 1)
        header = header.strip()
        value = value.strip()
        filtered_data = [self.headers]

        # Проверяю есть ли переданный столбец в таблице
        if header not in self.headers:
            raise ValueError(f"Столбец '{header}' не найден в данных")
        column_index = self.headers.index(header)

        # Сравниваю переданное значение с значением в каждой строке
        for row in data[1:]:
            if actions[ordered_action](row[column_index], value):
                filtered_data.append(row)
        if len(filtered_data) == 1:
            raise ValueError(f"Нет данных подходящих под условия фильтра")
        return filtered_data

    def aggregate_data(self, condition: str, data: list[list[str]]) -> list[list[str]]:
        actions = {
            'avg': lambda x: sum(x) / len(x) if x else 0.0,
            'min': lambda x: min(x) if x else 0.0,
            'max': lambda x: max(x) if x else 0.0
        }
        if '=' not in condition:
            raise ValueError("Формат условия должен быть header=action, например rating=avg")

        # Разделяю переданную строку
        header, action = condition.split('=', 1)
        header = header.strip()
        action = action.strip()

        # Ищу есть ли в переданной строке доступное действие
        if action not in actions:
            raise ValueError(f"Неподдерживаемое условие агрегации: {action}. Используйте одно из: {list(actions.keys())}")

        # Проверяю есть ли переданный столбец в таблице
        if header not in self.headers:
            raise ValueError(f"Столбец '{header}' не найден в данных")
        column_index = self.headers.index(header)

        # Проверяю является ли значение в строке числом
        try:
            values = [float(row[column_index]) for row in data[1:]]
        except ValueError:
            raise ValueError(f"Столбец '{header}' содержит нечисловые значения")

        result = actions[action](values)
        aggregated_data = [[action], [result]]
        return aggregated_data

    def display_data(self, data: list[list[str]]) -> str:
        return tabulate(data[1:], headers=data[0], tablefmt="outline")


def main() -> str:
    try:
        parser = argparse.ArgumentParser(description='Обработка CSV файлов')
        parser.add_argument(
            '--file', help='Имя файла если он в той же директории иили абсолютный путь в кавычках'
        )
        parser.add_argument(
            '--where', metavar='condition',
            help='Фильтрация данных. Например python main.py --file data.csv --where "brand=apple"'
        )
        parser.add_argument(
            '--aggregate', metavar='condition',
            help='Агрегация данных. Например python main.py --file data.csv --aggregate "rating=avg"'
        )

        args = parser.parse_args()
        processor = CSVProcessor(args.file)

        if args.where and args.aggregate:
            filtered_data = processor.filter_data(args.where, processor.data)
            aggregated_data = processor.aggregate_data(args.aggregate, filtered_data)
            return processor.display_data(aggregated_data)

        if args.where:
            filtered_data = processor.filter_data(args.where, processor.data)
            return processor.display_data(filtered_data)

        if args.aggregate:
            aggregated_data = processor.aggregate_data(args.aggregate, processor.data)
            return processor.display_data(aggregated_data) 

        return processor.display_data(processor.data)
    except Exception as error:
        return f"{error}"


if __name__ == "__main__":
    print(main())
