import sys
import os
import unittest
import unittest.mock as mock
import json
sys.path.append(os.path.join(os.getcwd(), '..'))
import common.functions as functions
import common.constants as constants


class TestSocket:
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message_to_send):
        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode(constants.DECODING_FORMAT)
        self.received_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(constants.DECODING_FORMAT)


class TestUtils(unittest.TestCase):
    test_dict_send = {
        "action": "presence",
        "time": 1.5,
        "type": "status",
        "user": {
            "account_name": "test_user",
            "status": "Status report"
        }
    }

    test_dict_recv_ok = {
        "response": 200,
        "alert": "OK"
    }

    test_dict_recv_err = {
        "response": 500,
        "error": "ошибка сервера"
    }

    def test_send_message(self):
        test_socket = TestSocket(self.test_dict_send)
        functions.send_message(test_socket, self.test_dict_send)
        self.assertEqual(test_socket.encoded_message, test_socket.received_message)
        self.assertRaises(TypeError, functions.send_message, test_socket, "wrong_dictionary")

    def test_get_message(self):
        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        test_sock_err = TestSocket(self.test_dict_recv_err)
        self.assertEqual(functions.get_message(test_sock_ok), self.test_dict_recv_ok)
        self.assertEqual(functions.get_message(test_sock_err), self.test_dict_recv_err)

    def test_def_presence_equal(self):
        test = functions.presence_message("")
        test["time"] = 1.2
        self.assertEqual(test, {"action": "presence", "time": 1.2, "type": "status",
                                "user": {"account_name": '', "status": "Status report"}})

    def test_def_presence_not_equal(self):
        test = functions.presence_message("")
        test["time"] = 1.1
        self.assertNotEqual(test, {"action": "presence", "time": 1.1,
                                   "user": {"account_name": '', "status": "Status report"}})

    def test_def_presence_server_200_ans(self):
        self.assertEqual(functions.presence_server({"response": 200, "alert": "OK"}), '200 : OK')

    def test_def_presence_server_200_wrong_ans(self):
        self.assertNotEqual(functions.presence_server({"response": 200, "alert": "OK"}),
                            '200 : неправильный запрос,JSON - объект')

    def test_def_presence_server_400_ans(self):
        self.assertEqual(functions.presence_server({"response": 400, "error": "неправильный запрос,JSON - объект"}),
                         '400 : неправильный запрос,JSON - объект')

    def test_def_presence_server_400_wrong_ans(self):
        self.assertNotEqual(functions.presence_server({"response": 400, "error": "неправильный запрос,JSON - объект"}),
                            '200 : OK')

    def test_sys_ip_validation(self):
        test_sys_args_ip = "176.0.0.1"
        with mock.patch('sys.argv', test_sys_args_ip):
            self.assertEqual(functions.sys_ip_validation(sys.argv), None)

    def test_sys_ip_validation_error(self):
        test_sys_args_ip_err = "1761.0.0.1"
        with mock.patch('sys.argv', test_sys_args_ip_err):
            with self.assertRaises(SystemExit):
                functions.sys_ip_validation(sys.argv)


if __name__ == '__main__':
    unittest.main()
