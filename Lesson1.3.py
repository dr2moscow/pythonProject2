# Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.

# записать в байтовом типе:

words = ['attribute', 'класс', 'функция', 'type']
words_invalid = []


for el in words:
    byte = el.encode()
    if '\\' in str(byte):
        words_invalid.append(el)
print(f'Невозможно записать в байтовом типе слова: {", ".join(words_invalid)}')
