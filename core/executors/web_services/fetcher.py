import grequests
import requests
from core.utils import log_process

print("--- { FETCHER LOADED } ---")


class Fetcher:
    @staticmethod
    def fetch(*urls, **kwargs):
        for u in urls:
            assert isinstance(u, str)
            print("Fetching async url:", u[:100])

        requests = (grequests.get(u, **kwargs) for u in urls)
        responses = grequests.map(requests, exception_handler=lambda r, e: log_process("EXCEPTION OCCURED WHILE FETCHING",r, e))

        log_process("Responses", responses)
        for r in responses:
            if r is not None and not r.ok:
                log_process("Response", r, "is not ok", r.reason)

        return responses

    @staticmethod
    def fetchOne(url, **kwargs):
        log_process("Fetching url:", url)
        response = requests.get(url, **kwargs)

        log_process("Response", response)
        if (response is not None and not response.ok):
                log_process("Response", response, "is not ok", response.reason)

        return response