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
        instance.getDefinitions.return_value = [mock, mock, mock]
        original_call = wordnik.WordApi.WordApi().getDefinitions()
        assert len(instance.getDefinitions()) == len(original_call)
        for test_mock in original_call:
            assert test_mock == mock

if __name__ == '__main__':
    unittest.main()
