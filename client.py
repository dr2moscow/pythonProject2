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
from errors import ReqFieldMissingError
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, DEFAULT_PORT, ERROR, DEFAULT_IP_ADDRESS
from common.utils import get_message, send_message

# Инициализация клогера
logger = logging.getLogger('client')


class Client:
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
            logger.info(f'Принят ответ от сервера {answer}')
            print(answer)
        except json.JSONDecodeError:
            logger.error(f'Не удалось декодировать полученную Json строку.')
        except ConnectionRefusedError:
            logger.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                            f'конечный компьютер отверг запрос на подключение.')
        except ReqFieldMissingError as missing_error:
            logger.error(f'В ответе сервера отсутствует необходимое поле '
                         f'{missing_error.missing_field}')
        sys.exit(1)

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
        logger.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
        return out

    def process_answer(message):
        """
        Функция разбирает ответ сервера
        :param message:
        :return:
        """
        logger.debug(f'Разбор сообщения от сервера: {message}')
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return '200 : OK'
            return f'400 : {message[ERROR]}'
        raise ReqFieldMissingError(RESPONSE)

    @staticmethod
    def create_arg_parser():
        """
        Создаём парсер аргументов коммандной строки
        :return:
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
        parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
        return parser


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
        logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    logger.info(f'Запущен клиент с парамертами: адрес сервера: '
                f'{server_address} , порт: {server_port}')

    # Создадем клиент
    client_connect = Client(server_address, server_port)
    client_connect.message_send(Client.status_presence)


if __name__ == "__main__":
    main()
