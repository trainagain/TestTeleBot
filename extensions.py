import json
import requests
from config import keys

class APIException(Exception):
    pass

class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")
        try:
            quote_key = keys[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")
        if base_key == quote_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')
        r = requests.get(f'https://www.cbr-xml-daily.ru/latest.js')
        t_base = json.loads(r.content)['rates']
        t_base['RUB'] = 1
        total_base = float(t_base[quote_key])/float(t_base[base_key]) * amount
        total_base = round(total_base, 3)
        message = f'Цена {amount} {base} в {quote} - {total_base}'
        return message
