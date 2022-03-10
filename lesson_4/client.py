import socket
import sys
import json
import common.functions as functions
import common.constants as constants


def main():
    try:
        server_address = "1271.0.0.1"
        functions.sys_ip_validation(server_address)
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = constants.DEFAULT_ADDRESS
        server_port = constants.DEFAULT_PORT
    except ValueError:
        print('Только числа в диапазоне от 1024 до 65535.')
        sys.exit(1)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_address, server_port))
    message = functions.presence_message(account_name)
    functions.send_message(client, message)
    try:
        answer = functions.presence_server(functions.get_message(client))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    account_name = "default_user"
    main()
