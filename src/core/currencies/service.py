from src.core.currencies.model import Currencies


class CurrencyService:
    def __init__(self):
        ...

    @classmethod
    def get_currency_from_address(cls, address: str):
        for currency in Currencies:
            if address.startswith(currency.value.PREFIX):
                return currency.value.PREFIX
        raise ValueError(f"No currency found for address '{address}'.")
