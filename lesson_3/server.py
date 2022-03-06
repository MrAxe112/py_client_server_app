import socket
import json
import sys
import common.functions as functions
import common.constants as constants


def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = constants.DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        print(
            'В качастве порта только числа в диапазоне от 1024 до 65535.')

    try:
        if '-a' in sys.argv:
            listen_addr = sys.argv[sys.argv.index('-a') + 1]
            functions.sys_ip_validation(listen_addr)
        else:
            listen_addr = ""
    except IndexError:
        print(
            'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((listen_addr, listen_port))
    server.listen(constants.MAX_CLIENTS)

    while True:
        client, adr = server.accept()
        try:
            message_from_client = functions.get_message(client)
            # print(message_from_client)
            response = functions.presence_message_validation(message_from_client)
            functions.send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
