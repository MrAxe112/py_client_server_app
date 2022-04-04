import sys
import time
import json
import common.constants as constants
import common.alerts
from socket import inet_aton
from socket import error as s_error
from common.decorators import log


@log
def message_presence(user_name):
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


@log
def message_common(user_name, text, send_to):
    chat_msg = {
        "action": "msg",
        "time": time.time(),
        "to": send_to,
        "from": user_name,
        "message": str(text),
    }
    return chat_msg


@log
def send_message(sock, message):
    if not isinstance(message, dict):
        raise TypeError
    json_message = json.dumps(message)
    encoded_message = json_message.encode(constants.DECODING_FORMAT)
    sock.send(encoded_message)


@log
def get_message(client):
    encoded_response = client.recv(constants.MAX_LENGTH_BYTES)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(constants.DECODING_FORMAT)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


@log
def presence_message_validation(message):
    if "action" in message and message["action"] == 'presence' and "time" in message and "type" in message \
            and message["type"] == "status" and "account_name" in message["user"] and "status" in message["user"]:
        return common.alerts.alert_200
    return common.alerts.alert_400


@log
def presence_server(message):
    if "response" in message:
        if message["response"] == 200:
            return '200 : OK'
        return f'400 : {message["error"]}'
    raise ValueError


@log
def sys_ip_validation(address):
    try:
        inet_aton(str(address))
    except s_error:
        print("ip адрес не правильный")
        sys.exit(1)


@log
def message_type_separation(client, message_obj, messages_list):
    if "action" in message_obj and message_obj["action"] == "presence":
        presence = presence_message_validation(message_obj)
        send_message(client, presence)
        return

    elif "action" in message_obj and message_obj["action"] == "msg" \
            and "time" in message_obj and "message" in message_obj:
        messages_list.append((message_obj["from"], message_obj["message"], message_obj["to"]))
        return

    else:
        send_message(client, {
            "response": 400,
            "error": 'Bad Request'
        })
        return
