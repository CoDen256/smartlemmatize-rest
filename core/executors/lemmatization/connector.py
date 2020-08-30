from collections.abc import Iterable
from core.data import PartOfSpeech

VERBS_TO_IGNORE = ["müssen", "sollen", "können", "dürfen", "sein", "haben", "werden", "wollen", "sein_es", "lassen"]


class LemmaConnector:

    def connect(self, sentences):
        connected = [self.connect_lemmas(sentence) for sentence in sentences]
        return self.remove_special(self.unpack(connected))

    def connect_lemmas(self, lemmata):
        last_verb = None
        last_refl = None
        last_prefix = None

        for pos in lemmata:
            main = pos.main
            word_type = pos.wordType
            orig = pos.original

            if word_type in ["$,", "$."] or word_type == "KON":
                # print("STARTING UPDATE", lastVerb)
                # if (lastVerb != None):
                #    print(lastVerb.toJson(), lastPrefix, lastRefl)

                self.update(last_verb, last_prefix, last_refl)
                last_verb = None
                last_refl = None
                last_prefix = None
                continue

            if word_type.startswith("V") and main not in VERBS_TO_IGNORE:
                # print("VERB", pos.toJson())
                last_verb = pos

            if word_type.startswith("PRF"):
                # print("REFLEX:", pos.toJson())
                last_refl = pos

            if word_type.startswith("PTKVZ"):
                # print("PREFIX", pos.toJson())
                last_prefix = pos

        return lemmata

    @staticmethod
    def update(verb, prefix, refl):
        if verb is None: return

        verb.args["prefix"] = ""

        if prefix is not None:
            verb.args["prefix"] = prefix.main

        if refl is not None:
            verb.args["reflex"] = True

    @staticmethod
    def remove_special(unpacked):
        result = []
        for lemma in unpacked:
            if lemma.wordType not in ["$,", "$.", "$(", "CARD", "FM.xy"] and lemma.original.replace('\'', '').isalpha():
                result.append(lemma)
        return result

    @staticmethod
    def unpack(connected):
        unpacked = []
        for sentence in connected:
            for lemma in sentence:
                unpacked.append(lemma)
        return unpacked