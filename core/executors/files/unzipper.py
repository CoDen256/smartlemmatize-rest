
class Gzipper:
    def unzip(self, data):
        import gzip
        return gzip.decompress(data)


