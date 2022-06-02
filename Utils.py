import requests
import json
from config import keys


class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно конвертировать одинаковые валюты {base}')

        try:
            quote_ticken = keys[quote]
        except KeyError:
            raise APIException(f'Извините, {quote}- такой валюты нет в списке.')

        try:
            base_ticken = keys[base]
        except KeyError:
            raise APIException(f'Извините, {base}- такой валюты нет в списке.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Извините, не удалось обработать количество {amount}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticken}&tsyms={base_ticken}')
        total_base = float(json.loads(r.content)[keys[base]])
        return total_base
