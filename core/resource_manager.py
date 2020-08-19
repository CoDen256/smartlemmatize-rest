import os
from core.utils import assertType

class Resource:
    def __init__(self, name, path, template):
        self.name = name
        self.absolute_folder = os.path.abspath(path) + "/"

        self._template = template
        
    def get_absolute_path(self, **kwargs):
        return self.absolute_folder + self._template.format(**kwargs)

class ResourceManager:
    PATH = "resources/"

    LTC = Resource("LEMMATIZED_TIME_CODE", PATH+"ltc/", 'ltc_{id}_s{s}_ep{e}.json')
    SRT = Resource("SUBTITLE_SCRIPT", PATH+"srt/", 'script_{id}_s{s}_ep{e}.srt')

    resources = [LTC, SRT]

    CACHE = {}

    @staticmethod
    def exists(resource, query):
        if resource not in ResourceManager.resources: raise Exception("RESOURCE NOT FOUND: " + resource.name)
        assertType("possiblyExistingResource", resource, Resource)

        return os.path.exists(ResourceManager.path(resource, query))

    @staticmethod
    def path(resource, query):
        if resource not in ResourceManager.resources: raise Exception("RESOURCE NOT FOUND: " + resource.name)
        assertType("withPathResource", resource, Resource)

        return resource.get_absolute_path(id=query.id, e=query.episode, s=query.season)

    def setLastLoaded(resource, content):
        assertType("lastLoadedResourceOnSet", resource, Resource)
        ResourceManager.CACHE[resource] = content
    
    def getLastLoaded(resource):
        assertType("lastLoadedResourceOnGet", resource, Resource)
        return CACHE[resource]





