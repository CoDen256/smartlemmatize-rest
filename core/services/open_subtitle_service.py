from fetcher import Fetcher
from core.data.request import Request
from core.utils import assertType

class OpenSubtitleService:
    URL = f"https://rest.opensubtitles.org/search/"+\
          "episode-{EPISODE}/imdbid-{ID}/season-{SEASON}/sublanguageid-ger"

    HEADERS = {"X-User-Agent": "codenua"}
    INFO_FORMAT = "BluRay"

    @staticmethod
    def fetch(request):
        assertType("request to fetch", request, Request)
        result_url = OpenSubtitleService.URL.format(EPISODE = request.episode,
                                SEASON = request.season,
                                ID = request.id)

        response = Fetcher.fetchOne(result_url, headers=OpenSubtitleService.HEADERS)

        if (response is None or not response.ok):
            raise Exception("Unable to fetch opensubtitles link, abort")
        link = OpenSubtitleService.find_download_link(response.json())

        download_reponse = Fetcher.fetchOne(link, headers=OpenSubtitleService.HEADERS)

        if (download_reponse is None or not download_reponse.ok):
            raise Exception("Unable to fetch download opensubtitles link, abort")

        return download_reponse.content

    @staticmethod
    def find_download_link(response):
        for source in response:
            if source["InfoFormat"] == OpenSubtitleService.INFO_FORMAT:
                return source["SubDownloadLink"]

        raise Exception("Download link not found")