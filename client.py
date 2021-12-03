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
import argparse
import logging
import logs.config_client_log
from common.variables import ACTION, TIME, USER, ACCOUNT_NAME, RESPONSE, \
    DEFAULT_IP_ADDRESS, DEFAULT_PORT, ERROR, PRESENCE
from common.utils import get_message, send_message
from errors import ReqFieldMissingError
from decorators import log

LOGGER = logging.getLogger('client')


class Client:
    @log
    def __init__(self, server_address, server_port):
        self.address = server_address
        self.port = server_port
        try:
            # Инициализация сокета и обмен
            self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.transport.connect((self.address, self.port))
            message_to_server = Client.status_presence()
            send_message(self.transport, message_to_server)
            answer = Client.process_answer(get_message(self.transport))
            LOGGER.info(f'Принят ответ от сервера {answer}')
            print(answer)
        except json.JSONDecodeError:
            LOGGER.error(f'Не удалось декодировать полученную Json строку.')
        except ConnectionRefusedError:
            LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                         f'конечный компьютер отверг запрос на подключение.')
        except ReqFieldMissingError as missing_error:
            LOGGER.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        sys.exit(1)

    @log
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
        LOGGER.info(f'Генерим запрос о присуттсвии: {out}')
        return out

    @log
    def process_answer(message):
        """
        Функция разбирает ответ сервера
        :param message:
        :return:
        """
        LOGGER.info(f'Разбор сообщения от сервера: {message}')
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return '200 : OK'
            return f'400 : {message[ERROR]}'
        raise ValueError


    @log
    def create_arg_parser():
        """
        Создаём парсер аргументов коммандной строки
        :return:
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
        parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
        LOGGER.debug(f'Создаём парсер аргументов коммандной строки: {parser}')
        return parser


@log
def main():
    """
    Загружаем параметы коммандной строки
    """
    parser = Client.create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        log.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)
    # Создадем клиент
    LOGGER.info(f'Запущен клиент с парамертами: адрес сервера: {server_address}, порт: {server_port}')
    client_connect = Client(server_address, server_port)
    client_connect.message_send(Client.status_presence)


if __name__ == "__main__":
    main()