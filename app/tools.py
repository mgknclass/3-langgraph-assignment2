from loguru import logger
from app.config import settings
from langchain.tools import tool
from langchain_core.tools import InjectedToolArg
from typing import Annotated
import requests


@tool
def convert(
    base_currency_value: int, conversion_rate: Annotated[float, InjectedToolArg]
) -> float:
    """
    given a currency conversion rate this function calculates the target currency value from a given base currency value
    """
    return base_currency_value * conversion_rate


@tool
def get_conversion_factor(base_currency: str, target_currency: str) -> float:
    """
    Given a base currency and target currency
    this tool will return the conversion factor
    """
    url = f"https://v6.exchangerate-api.com/v6/{settings.exchangerate_api_key}/pair/{base_currency}/{target_currency}"
    resp = requests.get(url)
    return resp.json()
