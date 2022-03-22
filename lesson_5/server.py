import socket
import json
import sys
import logging
import logs.config_server_log
import common.functions as functions
import common.constants as constants

server_log = logging.getLogger('server')


def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = constants.DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        server_log.error(f'Попытка запуска сервера с указанием неподходящего порта.'
                         f'После параметра -\'p\' необходимо указать номер порта. ')
        sys.exit(1)
    except ValueError:
        server_log.error(f'Попытка запуска сервера с указанием неподходящего порта '
                         f'{listen_port}. Допустимы адреса с 1024 до 65535.')

    try:
        if '-a' in sys.argv:
            listen_addr = sys.argv[sys.argv.index('-a') + 1]
            functions.sys_ip_validation(listen_addr)
        else:
            listen_addr = ""
    except IndexError:
        server_log.error(f'Попытка запуска сервера с указанием неподходящего адреса.'
                         f'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)
    server_log.info(f'Запущен сервер, порт для подключений: "{listen_port}", '
                    f'адрес с которого принимаются подключения: "{listen_addr}". '
                    f'Если адрес не указан, принимаются соединения с любых адресов.')

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((listen_addr, listen_port))
    server.listen(constants.MAX_CLIENTS)

    while True:
        client, adr = server.accept()
        try:
            message_from_client = functions.get_message(client)
            server_log.debug(f"сообщение от клиента: '{message_from_client}'")
            response = functions.presence_message_validation(message_from_client)
            server_log.debug(f"сформированный ответ: '{response}'")
            functions.send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            server_log.error(f'Некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
