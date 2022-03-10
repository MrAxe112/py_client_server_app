import sys
import time
import json
import common.constants as constants
import common.alerts
from socket import inet_aton
from socket import error as s_error


def presence_message(user_name):
    client_presence = {
        "action": "presence",
        "time": time.time(),
        "type": "status",
        "user": {
            "account_name": user_name,
            "status": "Status report"
        }
    }
    return client_presence


def send_message(sock, message):
    if not isinstance(message, dict):
        raise TypeError
    json_message = json.dumps(message)
    encoded_message = json_message.encode(constants.DECODING_FORMAT)
    sock.send(encoded_message)


def get_message(client):
    encoded_response = client.recv(constants.MAX_LENGTH_BYTES)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(constants.DECODING_FORMAT)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def presence_message_validation(message):
    if "action" in message and message["action"] == 'presence' and "time" in message and "type" in message \
            and message["type"] == "status" and "account_name" in message["user"] and "status" in message["user"]:
        return common.alerts.alert_200
    return common.alerts.alert_400


def presence_server(message):
    if "response" in message:
        if message["response"] == 200:
            return '200 : OK'
        return f'400 : {message["error"]}'
    raise ValueError


def sys_ip_validation(address):
    try:
        inet_aton(str(address))
    except s_error:
        print("ip адрес не правильный")
        sys.exit(1)

