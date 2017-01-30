"""
This code solve test task:
- Logon via QuikFixAdapter
- Buy stock of Lukoil
"""

from api import Client, FIXProtocol
import random

# First part
client = Client()
client.connect_to_adapter("127.0.0.1", 9000)

protocol = FIXProtocol()
request = protocol.build_request({"BeginString": "FIX.4.2",
                                  "BodyLength": 17,
                                  "MsgType": "A",
                                  "EncryptMethod": 0,
                                  "HearBitInt": 60,
                                  })
client.send_request(request)

# Second part
ord_id = "".join([random.choice("0123456789") for i in range(10)])
request = protocol.build_request({"BeginString": "FIX.4.2",
                                  "ClOrdID": ord_id,
                                  "MsgType": "D",
                                  "Side": 1,
                                  "OrdType": 1,
                                  "Price": 5000,  # It will be more than on market in the next several days, I thinks
                                  "IDSource": 8,
                                  "SecurityID": "LKOH",
                                  "Currency": "RUB",
                                  "OrderQty": 30,  # Count of money, summary, should be greater than 10**5
                                  "TimeInForce": 1,
                                  "ExDestination": "MICEX",
                                  "ClientID": "E5",
                                  })
client.send_request(request)

# Closing
client.close()
