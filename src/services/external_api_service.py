import requests
from typing import Optional, List
from requests.exceptions import RequestException
import logging

logger = logging.getLogger(__name__)

class ExchangeClient:
    """API client for couple exchange rates"""

    def __init__(self, api_urls: List[str]):
        self.api_urls = api_urls
        self.timeout = 10

    def get_exchange_rate(self, base: str, target: str) -> Optional[float]:
        cnt = 0
        for elem in self.api_urls:
            url = f"{elem}/{base}"
            cnt += 1
            try:
                logger.info(f"Attempt №{cnt}, request to {url}")
                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()
                rate = data.get("rates", {}).get(target)
                if rate is not None:
                    logger.info(f"Successfully got rate from url {url}")
                    return float(rate)
                else:
                    logger.warning(f"url {url} doesn't have {target}")
            except RequestException as e:
                logger.warning(f"Request error: {e}")
            except ValueError as e:
                logger.error(f"Invalid data: {e}")
        logger.error(f"All urls are unavailable or not contain {target}")
        return None
