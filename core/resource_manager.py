import os
from core.data.enums import Resource


class ResourceManager:
    PATH = "resources/"

    LTC = Resource("LEMMATIZED_TIME_CODE", PATH+"ltc/", 'ltc_{id}_s{s}_ep{e}.json')
    SRT = Resource("SUBTITLE_SCRIPT", PATH+"srt/", 'script_{id}_s{s}_ep{e}.srt')

    resources = [LTC, SRT]

    @staticmethod
    def exists(resource, query):
        if resource not in ResourceManager.resources: raise Exception("RESOURCE NOT FOUND: " + resource.name)
        assert isinstance(resource, Resource)

        return os.path.exists(ResourceManager.path(resource, query))

    @staticmethod
    def path(resource, query):
        if resource not in ResourceManager.resources: raise Exception("RESOURCE NOT FOUND: " + resource.name)
        assert isinstance(resource, Resource)

        return resource.get_absolute_path(id=query.id, e=query.episode, s=query.season)





