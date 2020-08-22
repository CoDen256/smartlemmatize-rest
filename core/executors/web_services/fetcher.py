import grequests
import requests
from core.utils import assertType, logProcess

print("[FETCHER LOADED]")

class Fetcher:
    @staticmethod
    def fetch(*urls, **kwargs):
        for u in urls:
            assertType("URL", u, str)
            print("Fetching async url:", u[:100])

        requests = (grequests.get(u, **kwargs) for u in urls)
        responses = grequests.map(requests, exception_handler=lambda r, e: logProcess("EXCEPTION OCCURED WHILE FETCHING",r, e))

        logProcess("Responses", responses)
        for r in responses:
            if (r is not None and not r.ok):
                logProcess("Response", r, "is not ok", r.reason)

        return responses

    @staticmethod
    def fetchOne(url, **kwargs):
        logProcess("Fetching url:", url)
        response = requests.get(url, **kwargs)

        logProcess("Response", response)
        if (response is not None and not response.ok):
                logProcess("Response", response, "is not ok", response.reason)

        return response