"""
3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле
YAML-формата. Для этого:
Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в кодировке
ASCII (например, €);
Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию файла
с помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
"""
import yaml

DATA_IN = {'items': ['книга', 'book', 'блокнот', 'notebook', 'карандаш'],
           'items_quantity': 5,
           'items_price': {
               'книга': '5Р-10Р',
               'book': '5$-10$',
               'блокнот': '30Р-70Р',
               'notebook': '30€-70€',
               'карандаш': '1\u20ac-2\u20ac'}
           }

with open('file.yaml', 'w', encoding='utf-8') as file_in:
    yaml.dump(DATA_IN, file_in, default_flow_style=False, allow_unicode=True, sort_keys=False)

with open('file.yaml', 'r', encoding='utf-8') as file_out:
    DATA_OUT = yaml.load(file_out, Loader=yaml.SafeLoader)

if DATA_IN == DATA_OUT:
    print('Данные совпадают!')