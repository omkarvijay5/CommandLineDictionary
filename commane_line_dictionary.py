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
        print "Definitions of the word %s are" % word
        for definition in definitions:
            print '* %s' % definition.text

    def get_synonyms(self, word):
        word_api = WordApi.WordApi(self.client)
        related_words = word_api.getRelatedWords(word)
        synonyms = []
        print "Synonyms of the word %s are" % word
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
        print "Antonyms of the word %s are" % word
        for related_word in related_words:
            if related_word.relationshipType == 'antonym':
                for word in related_word.words:
                    antonyms.append(word)
        for antonym in antonyms:
            print "* %s" % antonym

    def get_examples(self, word):
        word_api = WordApi.WordApi(self.client)
        examples = word_api.getExamples(word).examples
        print "Examples of the word %s are" % word
        for example in examples:
            print "* %s" % example.text

    def get_dictionary(self, word):
        self.get_definitions(word)
        self.get_synonyms(word)
        self.get_antonyms(word)
        self.get_examples(word)

    def get_word_of_the_day(self):
        pass


if __name__ == '__main__':
    class_object = CommandLineDict()
    if len(sys.argv) == 1:
        class_object.get_word_of_the_day()
    elif len(sys.argv) == 2:
        word = sys.argv[1]
        class_object.get_dictionary(word)
    elif sys.argv[1] == 'def':
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
