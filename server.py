"""
Server

Функции сервера: принимает сообщение клиента; формирует ответ клиенту; отправляет ответ клиенту;
имеет параметры командной строки:
-p <port> — TCP-порт для работы (по умолчанию использует 7777); -a <addr> — IP-адрес для прослушивания
(по умолчанию слушает все доступные адреса).

"""

import socket
import sys
import argparse
import json
import logging
import logs.config_server_log
from errors import IncorrectDataRecivedError
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, DEFAULT_PORT, MAX_CONNECTIONS, ERROR
from common.utils import get_message, send_message

# Инициализация логирования сервера.
logger = logging.getLogger('server')


class Server:
    def __init__(self, listen_address, listen_port):
        self.address = listen_address
        self.port = listen_port
        try:
            # Инициализация сокета и обмен
            self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.transport.bind((self.address, self.port))
        except BaseException:
            print("Ошибка!")
            sys.exit(1)

    def listen(self):
        """
        Слушваем порт
        """
        self.transport.listen(MAX_CONNECTIONS)
        while True:
            client, client_address = self.transport.accept()
            logger.info(f'Установлено соедение с ПК {client_address}')
            try:
                message_from_client = get_message(client)
                logger.debug(f'Получено сообщение {message_from_client}')
                response = self.process_client_message(message_from_client)
                logger.info(f'Сформирован ответ клиенту {response}')
                send_message(client, response)
                print(f'Принято корретное сообщение от клиента. {message_from_client}')
                logger.debug(f'Соединение с клиентом {client_address} закрывается.')
                client.close()
            except json.JSONDecodeError:
                logger.error(f'Не удалось декодировать Json строку, полученную от '
                                    f'клиента {client_address}. Соединение закрывается.')
                client.close()
            except IncorrectDataRecivedError:
                logger.error(f'От клиента {client_address} приняты некорректные данные. '
                                    f'Соединение закрывается.')
                client.close()

    @staticmethod
    def create_arg_parser():
        """
        Парсер аргументов коммандной строки
        :return:
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
        parser.add_argument('-a', default='', nargs='?')
        return parser

    @staticmethod
    def process_client_message(message):
        """
        Обработчик сообщений от клиентов, принимает словарь -
        сообщение от клинта, проверяет корректность,
        возвращает словарь-ответ для клиента

        :param message:
        :return:
        """
        logger.debug(f'Разбор сообщения от клиента : {message}')
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
                and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
            return {RESPONSE: 200}
        return {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }


def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8888 -a 127.0.0.1
    :return:
    """

    parser = Server.create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # проверка получения корретного номера порта для работы сервера.
    if not 1023 < listen_port < 65536:
        logger.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                        f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    logger.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                f'адрес с которого принимаются подключения: {listen_address}. '
                f'Если адрес не указан, принимаются соединения с любых адресов.')

    # Create server and listen
    server = Server(listen_address, listen_port)
    server.listen()


if __name__ == '__main__':
    main()
