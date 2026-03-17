# сервис отключен в этой версии

import requests
import time
from requests.exceptions import RequestException, Timeout, ConnectionError
from typing import Optional


class ExchangeClient:
    """API client for exchange rates"""

    def __init__(self, base_url: str = "https://api.exchangerate-api.com/v4/latest"):
        self.base_url = base_url
        self.timeout = 5
        self.max_retries = 3

    def get_exchange_rate(self, base: str, target: str) -> Optional[float]:
        delay = 1
        for attempt in range(self.max_retries):
            try:
                url = f"{self.base_url}/{base.upper()}"
                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()
                rates = data.get("rates", {})
                if target.upper() in rates:
                    return rates[target.upper()]
                else:
                    print(f"{target} not found")
            except Timeout:
                if attempt < self.max_retries - 1:
                    delay *= 2
                    print(f"Timeout (attempt {attempt + 1}, retrying in {delay} seconds)")
                    time.sleep(delay)
                else:
                    print("Timeout after all attempts")
                    return None
            except ConnectionError:
                if attempt < self.max_retries - 1:
                    delay *= 2
                    print(f"Connection error (attempt {attempt + 1}, retrying in {delay} seconds)")
                    time.sleep(delay)
                else:
                    print("Connection error after all attempts")
                    return None
            except RequestException as e:
                print(f"Request error: {e}")
                return None

        return None
