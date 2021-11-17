# Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
# Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
import locale

words = ['сетевое программирование', 'сокет', 'декоратор']

# создаем файл
with open('test.txt', 'w') as f:
    [f.write('\r'+el) for el in words]
    print(f'Файл {f.name} создан в кодировке по умолчанию {f.encoding} \n')

# Читаем из файла в кодровке по умоолчанию
with open('test.txt', 'r') as f:
    print(f'В кодировке по умолчанию {f.encoding}: {f.read()} \n')

# Читаем из файла принудииельтно в кодровке Unicode
with open('test.txt', 'r', encoding='utf-8', errors='replace') as f:
    print(f'В кодировка Unicode: {f.read()}')

print (f'\nВариант 2')
with open('test.txt', 'r', encoding=locale.getpreferredencoding()) as f:
    print(f'В кодировка Unicode: {f.read()}')
