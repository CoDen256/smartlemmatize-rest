import grequests

class Fetcher:
    @staticmethod
    def fetch(*urls, **kwargs):
        print("Fetching async urls:", urls)
        responses = (grequests.get(u, **kwargs) for u in urls)

        return grequests.map(responses)

    @staticmethod
    def fetchOne(url, **kwargs):
        print("Fetching url:", url)
        request = grequests.get(url, **kwargs)

        response = grequests.map([request])

        #if (response is not None and not response.ok):
        #    print("Response is not ok", response, reponse.reason)
        print("RESPONSE", response)
        return response