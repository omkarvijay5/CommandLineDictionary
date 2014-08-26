import unittest
import mock
import os
from mock import MagicMock
from wordnik import *
from command_line_dictionary import CommandLineDict
from mock import patch
import wordnik


class TestCommandLineDict(unittest.TestCase):

    def setUp(self):
        apiUrl = 'http://api.wordnik.com/v4'
        apiKey = os.environ['API_KEY']
        self.client = swagger.ApiClient(apiKey, apiUrl)
        self.test_object = CommandLineDict()

    @patch('wordnik.WordApi.WordApi')
    def test_get_definitions(self, mock_object):
        instance = mock_object.return_value
        mock = MagicMock()
        mock.text = 1
        instance.getDefinitions.return_value = [mock, mock, mock]
        original_call = self.test_object.get_definitions(mock)
        self.assertEqual(len(instance.getDefinitions()), len(original_call))
        self.assertEqual(original_call, [1, 1, 1])

if __name__ == '__main__':
    unittest.main()
