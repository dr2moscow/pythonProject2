# Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое
# и выполнить обратное преобразование (используя методы encode и decode).

words = ['разработка', 'администрирование', 'protocol', 'standard']


# решение через функцую
def convert(source: iter, mode, encoding='utf-8'):
    result = []
    for el in source:
        if mode == 'encode':
            result.append(el.encode(encoding))
        elif mode == 'decode':
            result.append(el.decode(encoding))
    return result


words_byte = convert(words, 'encode')
words_str = convert(words_byte, 'decode')

print(f'Байтовое представление: {words_byte}')
print(f'Стрроковое представление: {words_str}')
