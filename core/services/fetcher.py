import grequests

class Fetcher:
    @staticmethod
    def fetch(*urls):
        print("Fetching async urls:", urls)
        responses = (grequests.get(u) for u in urls)

        return grequests.map(responses)

    @staticmethod
    def fetchOne(url):
        print("Fetching url:", url)
        return grequests.get(url)