import os
import random
import sys
from wordnik import *
from wordnik.WordsApi import *


class CommandLineDict(object):

    def __init__(self):
        apiUrl = 'http://api.wordnik.com/v4'
        apiKey = os.environ['API_KEY']
        self.client = swagger.ApiClient(apiKey, apiUrl)
        self.antonyms = []
        self.synonyms = []
        self.definitions = []

    def get_definitions(self, word):
        word_api = WordApi.WordApi(self.client)
        definitions = word_api.getDefinitions(word, limit=50)
        return definitions

    def get_synonyms(self, word):
        word_api = WordApi.WordApi(self.client)
        related_words = word_api.getRelatedWords(word)
        synonyms = []
        if related_words:
            for related_word in related_words:
                if related_word.relationshipType == 'synonym':
                    for word in related_word.words:
                        synonyms.append(word)

        return synonyms

    def get_antonyms(self, word):
        word_api = WordApi.WordApi(self.client)
        related_words = word_api.getRelatedWords(word)
        antonyms = []
        if related_words:
            for related_word in related_words:
                if related_word.relationshipType == 'antonym':
                    for word in related_word.words:
                        antonyms.append(word)

        return antonyms

    def get_examples(self, word):
        word_api = WordApi.WordApi(self.client)
        examples = word_api.getExamples(word).examples
        if examples:
            print "Examples of the word %s are" % word
            for example in examples:
                print "* %s" % example.text
        else:
            print "No examples avaiable for the word %s" % word

    def get_dictionary(self, word):
        self.get_definitions(word)
        self.get_synonyms(word)
        self.get_antonyms(word)
        self.get_examples(word)

    def get_word_of_the_day(self):
        words_api = WordsApi(self.client)
        word_of_the_day = words_api.getWordOfTheDay().word
        print "The word of the day is %s" % word_of_the_day
        self.get_definitions(word_of_the_day)
        self.get_synonyms(word_of_the_day)
        self.get_antonyms(word_of_the_day)
        self.get_examples(word_of_the_day)

    def give_hint(self):
        pass

    def play(self):
        words_api = WordsApi(self.client)
        random_word = words_api.getRandomWord().word
        options = {0: 'get_synonyms', 1: 'get_antonyms', 2: 'get_definitions'}
        while True:
            random_num = random.choice([0, 1, 2])
            method = getattr(self, options[random_num])
            related_words = method(random_word)
            if related_words:
                related_word = related_words.pop()
                if hasattr(related_word, 'text'):
                    print "Definition of the word is given below \
                    answer the related word"
                    print "* %s" % related_word.text
                else:
                    print "Word is %s" % related_word
            else:
                jumbled_word = list(random_word)
                random.shuffle(jumbled_word)
                jumbled_word = ''.join(jumbled_word)
                print "jumbled word is %s" % jumbled_word
            entered_word = raw_input("Enter your answer")
            print "random word is", random_word
            if entered_word in related_words or entered_word == random_word:
                print "You win. You have entered correct word"
                break

    def display_words(self, resource_type, related_words, word):
        if related_words:
            print "{0} of the word {1} are".format(resource_type, word)
            if hasattr(related_words[0], 'text'):
                for definition in related_words:
                    print "* %s" % definition.text
            else:
                for word in related_words:
                    print "* %s" % word
        else:
            print "No {0} for the word {1}".format(resource_type, word)


if __name__ == '__main__':
    class_object = CommandLineDict()
    if len(sys.argv) == 1:
        class_object.get_word_of_the_day()
    elif sys.argv[1] == 'play':
        class_object.play()
    elif len(sys.argv) == 2:
        word = sys.argv[1]
        class_object.get_dictionary(word)
    elif sys.argv[1] == 'def':
        word = sys.argv[2]
        definitions = class_object.get_definitions(word)
        class_object.display_words('Definitions', definitions, word)
    elif sys.argv[1] == 'syn':
        word = sys.argv[2]
        synonyms = class_object.get_synonyms(word)
        class_object.display_words('Synonyms', synonyms, word)
    elif sys.argv[1] == 'ant':
        word = sys.argv[2]
        antonyms = class_object.get_antonyms(word)
        class_object.display_words('Antonyms', antonyms, word)
    elif sys.argv[1] == 'ex':
        word = sys.argv[2]
        class_object.get_examples(word)
