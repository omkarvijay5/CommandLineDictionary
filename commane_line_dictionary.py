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
        self.options = []

    def get_definitions(self, word):
        word_api = WordApi.WordApi(self.client)
        definitions = word_api.getDefinitions(word, limit=50)
        definitions = [definition.text for definition in definitions]
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

    def give_hint(self, word):
        random_options = [0, 1, 2, 3]
        for option in random_options:
            if option == 0:
                self.options.append(0)
            elif option == 1:
                self.definitions = self.get_definitions(word)
                if self.definitions:
                    self.options.append(1)
            elif option == 2:
                self.synonyms = self.get_synonyms(word)
                if self.synonyms:
                    self.options.append(2)
            elif option == 3:
                self.antonyms = self.get_antonyms(word)
                if self.antonyms:
                    self.options.append(3)
        if self.options:
            random_number = self.options.pop()
            if random_number == 0:
                jumbled_word = ''.join(random.shuffle(list(word)))
                print "jumbled answer is %s. \
                Try to guess the word", jumbled_word
            if random_number == 1:
                definition = self.definitions.pop()
                print "Definition is:"
                print "%s" % definition
                print "Try to guess the word"
            elif random_number == 2:
                synonym = self.synonyms.pop()
                print "Synonym is %s" % synonym
                print "Try to guess another synonym or antonym"
            elif random_number == 3:
                antonym = self.antonyms.pop()
                print "Antonym is %s" % antonym
                print "Try to guess another antonym or synonym"
        else:
            print "Sufficient hits have been given try to guess the word"

    def play(self):
        words_api = WordsApi(self.client)
        random_word = words_api.getRandomWord().word
        self.give_hint(random_word)
        while True:
            entered_word = raw_input("Enter your answer")
            print "random word is", random_word
            if entered_word in related_words or entered_word == random_word:
                print "You win. You have entered correct word"
                break

    def display_words(self, resource_type, related_words, word):
        if related_words:
            print "{0} of the word {1} are".format(resource_type, word)
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
