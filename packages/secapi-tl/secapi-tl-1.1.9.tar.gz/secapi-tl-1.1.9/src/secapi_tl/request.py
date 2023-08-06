"""
This module provides the sec_request function which must be used
for all requests to the  sec.gov domain to ensure that the amount
of requests stays in the boundaries set by the sec.
"""
import requests
from requests_random_user_agent import USER_AGENTS
from random import choice
from ratelimit import limits, sleep_and_retry
from threading import Semaphore

SEC_REQUEST_COUNT = 10
SEC_PERIOD = 1

SEMAPHORE = Semaphore(value=1)


@sleep_and_retry
@limits(calls=SEC_REQUEST_COUNT, period=SEC_PERIOD)
def sec_request(url: str):
    header = {"User-Agent": choice(USER_AGENTS)}
    SEMAPHORE.acquire()
    try:
        response = requests.get(url=url, headers=header)
        SEMAPHORE.release()
    except Exception as err:
        SEMAPHORE.release()
        raise err

    if response.status_code != 200:
        raise ConnectionError(f"invalid response status code {response.status_code}")
    return response
