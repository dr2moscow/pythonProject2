# Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
# (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.

# записать в байтовом типе:
words = [b'class', b'function', b'method']

[print(f'тип: {type(el)}, содержимое: {el}, текст: {str(el)[2:-1]}, динна: {len(el)}') for el in words]