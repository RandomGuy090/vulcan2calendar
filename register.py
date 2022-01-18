from vulcan import Keystore, Account
import asyncio

keystore = Keystore.create(device_model="vulcan2calendar")

with open("keystore.json", "w") as f:
    f.write(keystore.as_json)

pin = str(input("insert pin: "))
token = str(input("insert token: "))
symbol = str(input("insert symbol: "))
account=asyncio.get_event_loop().run_until_complete(Account.register(keystore, token, symbol, pin))

with open("account.json", "w") as f:
    f.write(account.as_json)

