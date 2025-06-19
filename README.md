# CSVReader
Скрипт, который помогает хранить считывать информацию
из csv-файлов, фильтровать или агрегировать данные.

## Используемый стэк
1. argparse
2. csv
3. pytest
4. pytest-cov
5. tabulate

## Как запустить проект локально
1. Установить и запустить вирутальное окружение

```
python -m venv venv
```
```
source venv/Scripts/activate
```

или

```
python3 -m venv venv
```
```
source venv/bin/activate
```

2. Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
3. Запустите скрипт
```
python main.py [-h] [--file FILE] [--where "condition"] [--aggregate "condition"]
```

Опциональные аргументы:
  --file file_name или "abs_file_path"
  Имя файла если он в той же директории иили абсолютный путь в кавычках.    
  --where "condition"
  Фильтрация данных. Например python main.py --file data.csv --where "brand=apple"    
  --aggregate "condition"
  Агрегация данных. Например python main.py --file data.csv --aggregate "rating=avg"

## Как запустить тесты
1. Находясь в корневой директории выполнить команду
   ```
   pytest -v
   ```

## Пример работы скрипта
![image](https://github.com/user-attachments/assets/713f4020-385b-4f2e-8abf-e72e39fa33ed)
