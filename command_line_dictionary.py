import os
import random
import sys
import pdb

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
        if definitions:
            definitions = [definition.text for definition in definitions]
            return definitions
        return []

    def get_synonyms(self, word):
        word_api = WordApi.WordApi(self.client)
        related_words = word_api.getRelatedWords(word)
        synonyms = []
        if related_words:
            for related_word in related_words:
                if related_word.relationshipType == 'synonym':
                    for word in related_word.words:
                        synonyms.append(word)
        synonyms = [synonym.lower() for synonym in synonyms]
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
        antonyms = [antonym.lower() for antonym in antonyms]
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

    def give_hint(self, word, from_hint=None):
        if not from_hint:
            random_options = [0, 1, 2, 3]
            for option in random_options:
                if option == 0:
                    self.options.append(0)
                if option == 1:
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
        if not self.definitions and 1 in self.options:
            self.options.remove(1)
        if not self.synonyms and 2 in self.options:
            self.options.remove(2)
        if not self.antonyms and 3 in self.options:
            self.options.remove(3)
        if self.options:
            random_number = random.choice(self.options)
            if random_number == 0 and from_hint:
                word_list = list(word)
                random.shuffle(word_list)
                jumbled_word = ''.join(word_list)
                print "jumbled word is %s. \
                Try to guess the word" % jumbled_word
                self.options.remove(0)
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
            entered_word = ''.join(entered_word.lower().split())
            if (entered_word in self.synonyms or
               entered_word in self.antonyms or entered_word == random_word):
                print "You win. You have entered correct word"
                break
            else:
                print "Oooops wrong answer... !!"
                print "select an option from below"
                print "1- Try again\n 2- Hint\n 3- Quit"
                option = raw_input("Enter an option")
                try:
                    option = int(option)
                except:
                    print "Enter a valid option"
                if option == 1:
                    pass
                elif option == 2:
                    from_hint = 1
                    self.give_hint(random_word, from_hint)
                elif option == 3:
                    print "Correct answer is %s" % random_word
                    synonyms = self.get_synonyms(random_word)
                    antonyms = self.get_antonyms(random_word)
                    self.display_words("Synonyms", synonyms, random_word)
                    self.display_words("Antonyms", antonyms, random_word)
                    self.get_dictionary(random_word)
                    print "See you soon"
                    break

    def display_words(self, resource_type, related_words, word):
        if related_words:
            print "{0} of the word {1} are".format(resource_type, word)
            for word in related_words:
                print word
        else:
            if resource_type is 'Definitions':
                words_api = WordsApi(self.client)
                search_words = words_api.searchWords(word)
                if search_words.totalResults == 0:
                    print "There are no definition for the word %s" % word
                else:
                    search_results = search_words.searchResults
                    search_words = [search_word.word for search_word in search_results]
                    print "There is no such word. Do you mean"
                    for word in search_words:
                        print "%s , " % word,
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
