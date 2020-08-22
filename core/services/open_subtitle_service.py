from fetcher import Fetcher
#from core.data.request import Request
#from core.utils import assertType

class OpenSubtitleService:
    URL = f"https://rest.opensubtitles.org/search/"+\
          "episode-{EPISODE}/imdbid-{ID}/season-{SEASON}/sublanguageid-ger"

    HEADER = {"X-User-Agent": "codenua"}
    INFO_FORMAT = "BlueRay"

    @staticmethod
    def fetch(request):
        #assertType("request to fetch", request, Request)
        result_url = OpenSubtitleService.URL.format(EPISODE = request.episode,
                                SEASON = request.season,
                                ID = request.id)

        response = Fetcher.fetchOne(result_url, header=OpenSubtitleService.HEADER)

        if (response is None or not response.ok):
            raise Exception("Unable to fetch opensubtitles link, abort")

        link = OpenSubtitleService.find_download_link(response.json())

        download_reponse = Fetcher.fetchOne(link, header=OpenSubtitleService.HEADER)

        if (download_reponse is None or not download_reponse.ok):
            raise Exception("Unable to fetch download opensubtitles link, abort")

        return download_reponse.content

    @staticmethod
    def find_download_link(response):
        for source in response:
            if source["InfoFormat"] == OpenSubtitleService.INFO_FORMAT:
                return source["SubDownloadLink"]

        raise Exception("Download link not found")



class TestRequest:
    def __init__(self, id, season, episode):
        self.id = id
        self.season = season
        self.episode = episode

if __name__ == "__main__":
    print(OpenSubtitleService.fetch(TestRequest(
        "0898266",1,1
    )))



