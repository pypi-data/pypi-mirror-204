"""
RiotAPICaller
Manages the waiting times and calls any given endpoint url.
"""

import time
from collections import deque
import requests


class RequestError(Exception):
    """
    RequestError is an Exception
    Raised when the RiotAPI sends an error code instead of 200
    """

    def __init__(self, in_status_code, in_text):
        self.status_code = in_status_code
        self.text = in_text
        msg = f"Request returned an error: {in_status_code} -> {in_text}."
        super().__init__(msg)


class BadRequest(Exception):
    """
    BadRequest is an Exception
    Raised when the RiotAPI sends error code 400
    """

    def __init__(self, in_status_code, in_text):
        self.status_code = in_status_code
        self.text = in_text
        msg = f"Request returned a error code 400 (Bad Request) -> {in_text}.\n"
        info = "Possible syntax Error in the request.\n" \
            "Common Reasons:\n" \
            "\t A provided parameter is in the wrong format (e.g., a string instead of an integer).\n" \
            "\t A provided parameter is invalid (e.g., beginTime and startTime specify a time range that is too large).\n" \
            "\t A required parameter was not provided.\n"
        super().__init__(msg + info)


class Unauthorized(Exception):
    """
    Unauthorized is an Exception
    Raised when the RiotAPI sends error code 401
    """

    def __init__(self, in_status_code, in_text):
        self.status_code = in_status_code
        self.text = in_text
        msg = f"Request returned a error code 401 (Unauthorized) -> {in_text}.\n"
        info = "Authentication error.\n" \
            "Common Reasons:\n" \
            "\t An API key has not been included in the request.\n"
        super().__init__(msg + info)


class Forbidden(Exception):
    """
    Forbidden is an Exception
    Raised when the RiotAPI sends error code 403
    """

    def __init__(self, in_status_code, in_text):
        self.status_code = in_status_code
        self.text = in_text
        msg = f"Request returned a error code 403 (Forbidden) -> {in_text}.\n"
        info = "Server understood the request but refuses to authorize it.\n" \
            "Common Reasons:\n" \
            "\t An invalid API key was provided with the API request.\n" \
            "\t A blacklisted API key was provided with the API request.\n" \
            "\t The API request was for an incorrect or unsupported path.\n"
        super().__init__(msg + info)


class NotFound(Exception):
    """
    NotFound is an Exception
    Raised when the RiotAPI sends error code 404
    """

    def __init__(self, in_status_code, in_text):
        self.status_code = in_status_code
        self.text = in_text
        msg = f"Request returned a error code 404 (Not Found) -> {in_text}.\n"
        info = "Server has not found a match for the API request being made.\n" \
            "Common Reasons:\n" \
            "\t The ID or name provided does not match any existing resource " \
               "(e.g., there is no Summoner matching the specified ID).\n" \
            "\t There are no resources that match the parameters specified.\n"
        super().__init__(msg + info)


class UnsupportedMediaType(Exception):
    """
    UnsupportedMediaType is an Exception
    Raised when the RiotAPI sends error code 415
    """

    def __init__(self, in_status_code, in_text):
        self.status_code = in_status_code
        self.text = in_text
        msg = f"Request returned a error code 415 (Unsupported Media Type) -> {in_text}.\n"
        info = "Server is refusing to service the request because the body of the request is in a format that is not supported.\n" \
            "Common Reasons:\n" \
            "\t The Content-Type header was not appropriately set.\n"
        super().__init__(msg + info)


class RateLimitExceeded(Exception):
    """
    RateLimitExceeded is an Exception
    Raised when the RiotAPI sends error code 429
    """

    def __init__(self, in_status_code, in_text):
        self.status_code = in_status_code
        self.text = in_text
        msg = f"Request returned a error code 429 (Rate Limit Exceeded) -> {in_text}.\n"
        info = "Application has exhausted its maximum number of allotted API calls allowed for a given duration.\n" \
            "Check the Retry-After header for number of seconds to wait.\n"
        super().__init__(msg + info)


class RiotAPICaller:
    """
    RiotAPICaller is the main class of this package.
    Keeps track of requests timers.
    """

    def __init__(self, in_app_config, in_last_use=120,
                 in_burst_size=20, in_burst_seconds=1, in_long_size=100, in_long_seconds=120):
        """
        Creates RiotAPICaller object which maintains queues to keep track of rate limits.
        Default values are set to match the Personal API Key rate limits.

        Parameters
        ----------
        in_app_config : AppConfig
            An AppConfig object that contains a valid RiotAPI key.
        in_last_use : float
            When (how many seconds ago) was the last time that a RiotAPI key was used.
            This value will be used for initializing the the rate limit maintaining.
        in_burst_size : int
            Size of the burst rate limit queue.
            in_burst_size requests per in_burst_seconds seconds
            e.g. 20 requests every 1 second
        in_burst_seconds : int
            Length of the burst rate limit queue in number of seconds.
            in_burst_size requests per in_burst_seconds seconds
            e.g. 20 requests every 1 second
        in_long_size : int
            Size of the long rate limit queue.
            in_long_size requests per in_long_seconds seconds
            e.g. 100 requests every 120 seconds (2 minutes)
        in_long_seconds : int
            Length of the long rate limit queue in number of seconds.
            in_long_size requests per in_long_seconds seconds
            e.g. 100 requests every 120 seconds (2 minutes)

        """
        self.config = in_app_config
        #
        # burst : in_burst_size requests per in_burst_seconds seconds
        self.burst_size = in_burst_size
        self.burst_seconds = in_burst_seconds
        self._burst_queue = deque(maxlen=in_burst_size)
        self._burst_queue.extend(
            (time.time() - in_last_use for i in range(in_burst_size)))
        #
        # long : in_long_size requests per in_long_seconds/60 minutes (in_long_seconds seconds)
        self.long_size = in_long_size
        self.long_seconds = in_long_seconds
        self._long_queue = deque(maxlen=in_long_size)
        self._long_queue.extend(
            (time.time() - in_last_use for i in range(in_long_size)))

    def _connect_to_endpoint(self, in_url, in_params):
        """
        Internal method for connecting to endpoint url with given parameters.

        Parameters
        ----------
        in_url : str
            URL of the endpoint
        in_params : dict
            A dictionary containing all the parameters and their values that needs to be sent

        Returns
        -------
        dict
            Returns the response JSON object as it is.

        Raises
        ------
        RequestError :
            The request returned a different status other than 200 (success).
        """
        response = requests.request("GET", in_url, headers={
                                    "X-Riot-Token": self.config.get_key()},
                                    params=in_params, timeout=3600)
        print(response.status_code)
        if response.status_code != 200:
            print(response)
            print(response.json())
            if response.status_code == 400:
                raise BadRequest(response.status_code, response.text)
            elif response.status_code == 401:
                raise Unauthorized(response.status_code, response.text)
            elif response.status_code == 403:
                raise Forbidden(response.status_code, response.text)
            elif response.status_code == 404:
                raise NotFound(response.status_code, response.text)
            elif response.status_code == 415:
                raise UnsupportedMediaType(response.status_code, response.text)
            elif response.status_code == 429:
                raise UnsupportedMediaType(response.status_code, response.text)
            else:
                raise RequestError(response.status_code, response.text)
        return response.json()

    def _wait_rate_limit(self):
        """
        Internal method that causes the program to
        wait (using time.sleep) for an appropriate amount of time.

        Returns
        -------
        None
        """
        # check long queue 1st
        current_time = time.time()
        long_elapsed_time = current_time - self._long_queue[0]
        burst_elapsed_time = current_time - self._burst_queue[0]
        max_wait = max(0, 120.0001 - long_elapsed_time, 1.0001 - burst_elapsed_time)
        if max_wait != 0:
            print(f"Waiting for : {max_wait}")
            time.sleep(max_wait)
            current_time = time.time()
        self._burst_queue.append(current_time)
        self._long_queue.append(current_time)

    def call_riot_api(self, in_url, in_params):
        """
        Waits for the appropriate amount of time and calls
        the end point given in the url with the given params.

        Parameters
        ----------
        in_url : str
            URL of the endpoint
        in_params : dict
            A dictionary containing all the parameters and their values that needs to be sent

        Returns
        -------
        dict
            Returns the response JSON object as it is.

        Raises
        ------
        RequestError :
            The request returned a different status other than 200 (success).
        """
        self._wait_rate_limit()
        json_response = self._connect_to_endpoint(in_url, in_params)
        return json_response
