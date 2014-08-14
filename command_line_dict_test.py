import unittest

from command_line_dictionary import CommandLineDict
from wordnik import *
from wordnik.WordsApi import *


class TestCommandLineDict(unittest.TestCase):

    def setUp(self):
        apiUrl = 'http://api.wordnik.com/v4'
        apiKey = os.environ['API_KEY']
        self.client = swagger.ApiClient(apiKey, apiUrl)


if __name__ == '__main__':
    unittest.main()
