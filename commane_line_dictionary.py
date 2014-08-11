import os
from wordnik import *
import sys


class CommandLineDict(object):

    def __init__(self):
        apiUrl = 'http://api.wordnik.com/v4'
        apiKey = os.environ['API_KEY']
        self.client = swagger.ApiClient(apiKey, apiUrl)

    def get_definitions(self, word):
        word_api = WordApi.WordApi(self.client)
        definitions = word_api.getDefinitions(word, limit=50)
        for definition in definitions:
            print '* %s' % definition.text

    def get_synonyms(self, word):
        word_api = WordApi.WordApi(self.client)
        related_words = word_api.getRelatedWords(word)
        synonyms = []
        for related_word in related_words:
            if related_word.relationshipType == 'synonym':
                for word in related_word.words:
                    synonyms.append(word)
        for synonym in synonyms:
            print "* %s" % synonym

    def get_antonyms(self, word):
        word_api = WordApi.WordApi(self.client)
        related_words = word_api.getRelatedWords(word)
        antonyms = []
        for related_word in related_words:
            if related_word.relationshipType == 'antonym':
                for word in related_word.words:
                    antonyms.append(word)
        for antonym in antonyms:
            print "* %s" % antonym

    def get_examples(self, word):
        word_api = WordApi.WordApi(self.client)
        examples = word_api.getExamples(word).examples
        for example in examples:
            print "* %s" % example.text


if __name__ == '__main__':
    class_object = CommandLineDict()
    if sys.argv[1] == 'def':
        word = sys.argv[2]
        class_object.get_definitions(word)
    elif sys.argv[1] == 'syn':
        word = sys.argv[2]
        class_object.get_synonyms(word)
    elif sys.argv[1] == 'ant':
        word = sys.argv[2]
        class_object.get_antonyms(word)
    elif sys.argv[1] == 'ex':
        word = sys.argv[2]
        class_object.get_examples(word)
