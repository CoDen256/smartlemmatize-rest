from core.data.request import Request


class OpenSubtitleService:
    URL = f"https://rest.opensubtitles.org/search/" + \
          "episode-{EPISODE}/imdbid-{ID}/season-{SEASON}/sublanguageid-ger"

    HEADERS = {"X-User-Agent": "codenua"}
    INFO_FORMAT = "BluRay"

    @staticmethod
    def fetch(request):
        from core.executors.web_services.fetcher import Fetcher
        assert isinstance(request, Request)
        result_url = OpenSubtitleService.URL.format(EPISODE=request.episode,
                                                    SEASON=request.season,
                                                    ID=request.id)

        response = Fetcher.fetchOne(result_url, headers=OpenSubtitleService.HEADERS)

        if response is None or not response.ok:
            raise Exception("Unable to fetch opensubtitles link, abort")
        link, encoding = OpenSubtitleService.find_download_link(response.json())

        encoding = encoding if encoding is not None else "CP1252"

        download_reponse = Fetcher.fetchOne(link, headers=OpenSubtitleService.HEADERS)

        if download_reponse is None or not download_reponse.ok:
            raise Exception("Unable to fetch download opensubtitles link, abort")

        return download_reponse.content, encoding

    @staticmethod
    def find_download_link(response):
        for source in response:
            if source["InfoFormat"] == OpenSubtitleService.INFO_FORMAT:
                return source["SubDownloadLink"], source["SubEncoding"]

        try:
            target = max(response, key=lambda r: int(r["SubDownloadsCnt"]))
            return target["SubDownloadLink"], target["SubEncoding"]
        except:
            raise Exception("Download link not found")

