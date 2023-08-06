"""
This module provides the sec_request function which must be used
for all requests to the  sec.gov domain to ensure that the amount
of requests stays in the boundaries set by the sec.

The method was implemented as a static method of a class because
an implementation as a normal function caused some issues
by exceeding the request limits when used with threading.
These issues disappeared with the implementation as a static method.
"""
import time
import math
import requests
from requests_random_user_agent import USER_AGENTS
from random import choice
from ratelimit import limits, sleep_and_retry

SEC_REQUEST_COUNT = 1
SEC_PERIOD = 0.1


class Request:

    @staticmethod
    @sleep_and_retry
    @limits(calls=SEC_REQUEST_COUNT, period=SEC_PERIOD)
    def sec_request(url: str, retries: int=5):
        header = {"User-Agent": choice(USER_AGENTS)}
        response = requests.get(url=url, headers=header)
        if response.status_code != 200 and retries > 0:
            time.sleep(20 * (1 / math.exp(retries-1)))
            response = Request.sec_request(url=url, retries=retries-1)

        # raise Connection error on deepest function call if there was no successful response for all tries
        if response.status_code != 200 and retries == 0:
            raise ConnectionError(f"invalid response statuscode: {response.status_code}")
        return response
