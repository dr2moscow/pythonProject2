"""
Client

Функции клиента: сформировать presence-сообщение; отправить сообщение серверу; получить ответ сервера;
разобрать сообщение сервера;

параметры командной строки скрипта client.py <addr> [<port>]: addr — ip-адрес сервера; port — tcp-порт на сервере,
по умолчанию 7777.
"""

import sys
import json
import socket
import time
from common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, \
    ERROR
from common.utils import get_message, send_message


class Client:
    def __init__(self, server_address, server_port):
        self.address = server_address
        self.port = server_port
        try:
            # Инициализация сокета и обмен
            self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.transport.connect((self.address, self.port))
        except BaseException:
            print("Ошибка!")
            sys.exit(1)

    @staticmethod
    def status_presence(account_name='Guest'):
        """
        Функция генерирует запрос о присутствии клиента
        :param account_name:
        :return:
        """
        out = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: account_name
            }
        }
        return out

    @staticmethod
    def process_answer(message):
        """
        Функция разбирает ответ сервера
        :param message:
        :return:
        """
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return '200 : OK'
            return f'400 : {message[ERROR]}'
        raise ValueError

    def message_send(self, message):
        """
        Функция по отправка сообщения
        :param message: тело сообщения
        """
        if message == PRESENCE:
            message_to_server = self.status_presence()
        else:
            sys.exit(0)
        send_message(self.transport, message_to_server)
        try:
            answer = self.process_answer(get_message(self.transport))
            print(answer)
        except (ValueError, json.JSONDecodeError):
            print(MESS_DECODE_ERROR)


def main():
    """
    Загружаем параметы коммандной строки
    """

    # Загружаем на какой порт сервера слать сообщение
    try:
        if '-p' in sys.argv:
            server_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            server_port = DEFAULT_PORT
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        print(
            'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Загружаем на какой адрес сервера слать сообщение
    try:
        if '-a' in sys.argv:
            server_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            server_address = DEFAULT_IP_ADDRESS
    except IndexError:
        print(
            'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    # Создадем клиент
    client_connect = Client(server_address, server_port)
    client_connect.message_send(PRESENCE)


if __name__ == "__main__":
    main()
