import argparse
import socket
import sys
import json
import logging
import logs.config_client_log
import common.functions as functions
import common.constants as constants

client_log = logging.getLogger('client')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default=constants.DEFAULT_ADDRESS, nargs='?')
    parser.add_argument('-p', default=constants.DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.a
    server_port = namespace.p
    client_mode = namespace.mode

    client_log.info(f'Запущен клиент с парамертами: адрес сервера: {server_address}, порт: {server_port}')

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_address, server_port))
    message = functions.message_presence(account_name)
    client_log.debug(f'Сообщение на присутствие {message}')
    functions.send_message(client, message)
    client_log.debug(f'Ответ от сервера на сообщение на присутствие '
                     f'{functions.presence_server(functions.get_message(client))}')

    if client_mode == 'send':
        print('Режим работы - отправка сообщений.')
    else:
        print('Режим работы - приём сообщений.')
    while True:
        if client_mode == 'send':
            while True:
                try:
                    text = input("Text: ")
                    if text == "exit":
                        sys.exit(1)
                    message_b = functions.message_common(account_name, text)

                    functions.send_message(client, message_b)
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    client_log.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)
        if client_mode == 'listen':
            try:
                response = functions.get_message(client)
                print(f'Сообщение от пользователя "{response["from"]}": "{response["message"]}"')
            except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                client_log.error(f'Соединение с сервером {server_address} было потеряно.')
                sys.exit(1)


if __name__ == '__main__':
    account_name = "default_user"
    main()
