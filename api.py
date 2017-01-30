from typecheck import *
import socket


class Client:
    def __init__(self):
        """
        This class will provide all connections to endpoint system using Quik Fix adapter.
        This class should allow an user to doesn't think about connections, only about actions as byu or sell.
        Also we use one client but with several reconnections to different servers.
            In this case, a coder can once create client and connect to adapter several times.
            So, initially, the method only create empty socket.
        """
        self.sock = None

    @typecheck
    def connect_to_adapter(self, ip: by_regex(r'''([0-9]{1,3}\.){3}[0-9]{1,3}'''), port: int) -> int:
        """
        This method provide connection to adapter.
        Use typechecker to check types for input data.
        :param ip: IPv4 string
        :param port: IP port
        :return: status of runtime (0 if all is ok else -1)
        """
        runtime_flag = 0
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((ip, port))
        except:
            runtime_flag = -1

        return runtime_flag

    @typecheck
    def send_request(self, request: str) -> int:
        """
        This method send the specific request to adapter.
        :param request: string with request
        :return: status of runtime (0 if all is ok else -1)
        """
        if not self.sock:
            raise ValueError("The client wasn't connected to adapter.")

        runtime_flag = 0
        try:
            b_string = bytes(request, encoding="utf-8")  # Convert string to bytes that allows to send socket
            self.sock.send(b_string)
        except:
            runtime_flag = -1

        return runtime_flag

    @typecheck
    def close(self) -> int:
        """
        The method for connection closing.
        :return: 0 if all is ok else -1
        """
        runtime_flag = 0
        try:
            self.sock.close()
        except:
            runtime_flag = -1
        return runtime_flag


class FIXProtocol:
    def __init__(self):
        """
        This class provides logic of request.
        A coder can send input dictionary with settings such as {'Price': 40} and class convert it using FIX protocol.
        Tags will store key-value pair of tags, i.e. MsgType - 35.
        A coder can supply tags too.
        """
        self.tags = {'BeginString': 8,
                     "BodyLength": 9,
                     "MsgType": 35,
                     "SenderCompID": 49,
                     "TargetCompID": 56,
                     "MsgSeqNum": 34,
                     "CheckSum": 10,
                     "EncryptMethod": 98,
                     "HearBitInt": 108,
                     "ClOrdID": 11,
                     "HandlInst": 21,
                     "Symbol": 55,
                     "Side": 54,
                     "OrdType": 40,
                     "Account": 1,
                     "Price": 44,
                     "IDSource": 22,
                     "SecurityID": 48,
                     "Currency": 15,
                     "OrderQty": 38,
                     "TimeInForce": 59,
                     "PartyID": 448,
                     "PartyIDSource": 447,
                     "PartyRole": 452,
                     "ExDestination": 100,
                     "ClientID": 109
                     }

    @typecheck
    def build_request(self, dictionary: dict_of(str, either(int, float, str))) -> str:
        """
        This method convert readable request's dictionary to request using FIX protocol.
        :param dictionary: string request
        :return: request by FIX protocol
        """
        result = []  # Store several tag's number and tag's value

        for k, v in dictionary.items():
            tag_value = self.tags.get(k, None)  # Check tag's name on inclusion in storage
            if tag_value is None:
                raise ValueError("{} is unknown.".format(k))
            else:
                result.append([tag_value, v])

        result_string = " | ".join(["=".join([str(cv) for cv in r]) for r in result])
        return result_string
