"""
This module provides the sec_request function which must be used
for all requests to the  sec.gov domain to ensure that the amount
of requests stays in the boundaries set by the sec.

The method was implemented as a static method of a class because
an implementation as a normal function caused some issues
by exceeding the request limits when used with threading.
These issues disappeared with the implementation as a static method.
"""
import requests
from requests_random_user_agent import USER_AGENTS
from random import choice
from ratelimit import limits, sleep_and_retry
from threading import Lock

SEC_REQUEST_COUNT = 1
SEC_PERIOD = 0.11


class Request:
    sec_request_lock = Lock()

    @staticmethod
    @sleep_and_retry
    @limits(calls=SEC_REQUEST_COUNT, period=SEC_PERIOD)
    def sec_request(url: str):
        header = {"User-Agent": choice(USER_AGENTS)}

        Request.sec_request_lock.acquire()
        response = requests.get(url=url, headers=header)
        Request.sec_request_lock.release()

        if response.status_code != 200:
            raise ConnectionError(f"invalid response status code {response.status_code}")
        return response
