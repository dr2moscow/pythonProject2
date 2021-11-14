# Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип на
# кириллице.

import subprocess
import chardet


# решение через функцую
def ping(target: str):
    args = ['ping', target]
    subp_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
    for el in subp_ping.stdout:
        codec = chardet.detect(el).get('encoding')
        print(el.decode(codec))


ping_resource = ['yandex.ru', 'youtube.com']

[ping(el) for el in ping_resource]
