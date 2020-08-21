from core.handlers.handler import AbstractHandler
from core.files import Writer
from core.utils import assertType

from collections.abc import Iterable
from core.data import PartOfSpeech

class LemmaConnector(AbstractHandler):
    def handle(self, request):

        connected = [self.connectLemmas(sentence) for sentence in request.getContent()]
        result =  self.removeSpecial(self.unpack(connected))

        request.setContent(result)

        Writer.write("4_lemma_connector.txt", result)
        return super().handle(request)


    def connectLemmas(self, lemmata): # only one sentence
        assertType("posLemmata", lemmata, Iterable)
        assertType("PartOfSpeech", lemmata[0], PartOfSpeech)

        lastVerb = None
        lastRefl = None
        lastPrefix = None
        verbsToIgnore = ["müssen", "sollen", "können", "dürfen", "sein", "haben", "werden", "wollen", "sein_es", "lassen"]
        
        for pos in lemmata:
            main = pos.main
            wType = pos.wordType
            orig = pos.original
            
            if (wType in ["$,","$."] or wType == "KON"):
                #print("STARTING UPDATE", lastVerb)
                #if (lastVerb != None):
                #    print(lastVerb.toJson(), lastPrefix, lastRefl)
                
                self.update(lastVerb, lastPrefix, lastRefl)
                
                lastVerb = None
                lastRefl = None
                lastPrefix = None
                continue
            
            if (wType.startswith("V") and main not in verbsToIgnore):
                #print("VERB", pos.toJson())
                lastVerb = pos
            
            if (wType.startswith("PRF")):
                #print("REFLEX:", pos.toJson())
                lastRefl = pos
                
            if (wType.startswith("PTKVZ")):
                #print("PREFIX", pos.toJson())
                lastPrefix = pos

        return lemmata


    def update(self, verb, prefix, refl):
        if (verb == None): return

        verb.args["prefix"] = ""

        if (prefix != None):
            verb.args["prefix"] = prefix.main;
		
        if (refl != None):
            verb.args["reflex"] = True;
        #print(verb.toJson())

    def unpack(self, connected):
        unpacked = []
        for sentence in connected:
            for lemma in sentence:
                unpacked.append(lemma)
        return unpacked

    def removeSpecial(self, unpacked):
        result = []
        for lemma in unpacked:
            if lemma.wordType not in ["$,","$."]:
                result.append(lemma)
        return result
        