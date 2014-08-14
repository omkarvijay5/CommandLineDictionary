import unittest

from command_line_dictionary import CommandLineDict
from wordnik import *
from wordnik.WordsApi import *


class TestCommandLineDict(unittest.TestCase):

    def setUp(self):
        apiUrl = 'http://api.wordnik.com/v4'
        apiKey = os.environ['API_KEY']
        self.client = swagger.ApiClient(apiKey, apiUrl)
        self.test_object = CommandLineDict()

    def test_get_synonyms(self):
        word = 'hello'
        synonyms = self.test_object.get_synonyms(word)
        self.assertEqual(len(synonyms), 10)

if __name__ == '__main__':
    unittest.main()
