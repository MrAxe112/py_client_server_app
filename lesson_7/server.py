import socket
import select
import json
import sys
import logging
import argparse
import logs.config_server_log
import common.functions as functions
import common.constants as constants

server_log = logging.getLogger('server')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=constants.DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_addr = namespace.a
    listen_port = namespace.p

    server_log.info(f'Запущен сервер, порт для подключений: "{listen_port}", '
                    f'адрес с которого принимаются подключения: "{listen_addr}". '
                    f'Если адрес не указан, принимаются соединения с любых адресов.')

    clients = []
    messages = []

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((listen_addr, listen_port))
    server.settimeout(0.5)
    server.listen(constants.MAX_CLIENTS)

    while True:
        try:
            new_client, address = server.accept()
        except OSError:
            pass
        else:
            clients.append(new_client)

        recv_data_list = []
        send_data_list = []
        try:
            if clients:
                recv_data_list, send_data_list, _ = select.select(clients, clients, [], 0)
        except OSError:
            pass
        if recv_data_list:
            for client_with_message in recv_data_list:
                try:
                    a = functions.get_message(client_with_message)
                    functions.message_type_separation(client_with_message, a, messages)
                except:
                    server_log.info(f'Клиент {client_with_message.getpeername()} '
                                    f'отключился от сервера.')
                    clients.remove(client_with_message)

        if messages and send_data_list:
            message = functions.message_common(messages[0][0], messages[0][1])
            del messages[0]
            for waiting_client in send_data_list:
                try:
                    functions.send_message(waiting_client, message)
                except:
                    server_log.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
