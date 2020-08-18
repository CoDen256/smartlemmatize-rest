class Resource:
    def __init__(self, name, path, resource_path):
        self.name = name
        self._path = path
        self._resource_path = resource_path

    def get_path(self):
        return self._path + self._resource_path

    def get_absolute_path(self):
        return self.get_path()

class ResourceManager:
    PATH = "resource/"

    LTC = Resource("LEMMATIZED_TIME_CODE", "ltc/", PATH)
    SRT = Resource("SUBTITLE_SCRIPT", "srt/", PATH)

    def __init__(self):
        self.resources = [self.LTC, self.SRT]

    def fetch_resource(self, resource, query, exists=False):
        if resource not in self.resources: raise Exception("RESOURCE NOT FOUND" + resource)

        if exists:
            return resource.get_absolute_path()
        else:
            return None 

