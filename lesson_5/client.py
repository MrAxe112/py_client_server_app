import socket
import sys
import json
import logging
import logs.config_client_log
import common.functions as functions
import common.constants as constants

client_log = logging.getLogger('client')


def main():
    try:
        # server_address = "121.0.0.1"
        # functions.sys_ip_validation(server_address)
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = constants.DEFAULT_ADDRESS
        server_port = constants.DEFAULT_PORT
    except ValueError:
        client_log.error('Попытка указать новый порт. Только числа в диапазоне от 1024 до 65535.')
        sys.exit(1)

    client_log.info(f'Запущен клиент с парамертами: '
                    f'адрес сервера: {server_address}, порт: {server_port}')

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_address, server_port))
    message = functions.presence_message(account_name)
    client_log.debug(f'Сообщение клиента {message}')
    functions.send_message(client, message)
    try:
        answer = functions.presence_server(functions.get_message(client))
        client_log.info(f'Ответ сервера: "{answer}"')
    except (ValueError, json.JSONDecodeError):
        client_log.error('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    account_name = "default_user"
    main()
