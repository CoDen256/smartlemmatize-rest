import grequests
import requests
from core.utils import assertType
class Fetcher:
    @staticmethod
    def fetch(*urls):
        for u in urls:
            assertType("URL", u, str)
            print("Fetching async url:", u[:100])

        requests = (grequests.get(u) for u in urls)
        responses = grequests.map(requests, exception_handler=lambda r, e: print("EXCEPTION OCCURED WHILE FETCHING",r, e))

        print("Responses", responses)
        return responses

    @staticmethod
    def fetchOne(url):
        print("Fetching url:", url)
        response = requests.get(url)
        print("Response", response)
        return response