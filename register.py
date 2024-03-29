from vulcan import Keystore, Account
import asyncio, json, os, sys

keystore = Keystore.create(device_model="vulcan2calendar")


keystore=asyncio.get_event_loop().run_until_complete(Keystore.create(device_model="vulcan2calendar"))

with open("keystore.json", "w") as f:
    f.write(keystore.as_json)

try:
    pin = os.environ.get("PIN") if os.environ.get("PIN")  else  str(input("insert pin: "))
    token = os.environ.get("TOKEN") if os.environ.get("TOKEN")  else str(input("insert token: "))
    symbol = os.environ.get("SYMBOL") if os.environ.get("SYMBOL")  else str(input("insert symbol: "))
except EOFError:
    print("use env variables or mount json files")
    print("use env variables or mount json files")
    print("use env variables or mount json files")
    print("_____________________________________")
    sys.exit(0)


print(f"{pin} {token} {symbol}")
account=asyncio.get_event_loop().run_until_complete(Account.register(keystore, token, symbol, pin))

with open("account.json", "w") as f:
    json.dump(account.as_dict, f)
    # f.write(account.as_json)

