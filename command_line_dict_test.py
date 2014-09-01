import unittest
import os
from mock import MagicMock
from wordnik import *
from mock import patch
import pdb
import sys
from StringIO import StringIO
from command_line_dictionary import CommandLineDict


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
        self.set_mock_and_test_definitions(mock, instance)

    @patch('wordnik.WordApi.WordApi')
    def test_get_synonyms(self, mock_object):
        instance = mock_object.return_value
        mock = MagicMock()
        self.set_mock_and_test_synonyms(mock, instance)

    @patch('wordnik.WordApi.WordApi')
    def test_get_antonyms(self, mock_object):
        instance = mock_object.return_value
        mock = MagicMock()
        self.set_mock_and_test_antonyms(mock, instance)

    @patch('wordnik.WordApi.WordApi')
    def test_get_example(self, mock_object):
        instance = mock_object.return_value
        mock = MagicMock()
        self.set_mock_and_test_examples(mock, instance)

    @patch('wordnik.WordApi.WordApi')
    def test_get_dictionary(self, mock_object):
        instance = mock_object.return_value
        mock = MagicMock()
        [mock, instance] = self.set_mock_and_test_antonyms(mock, instance)
        [mock, instance] = self.set_mock_and_test_synonyms(mock, instance)
        [mock, instance] = self.set_mock_and_test_definitions(mock, instance)
        [mock, instance] = self.set_mock_and_test_examples(mock, instance)
        saved_stdout = sys.stdout
        out = StringIO()
        sys.stdout = out
        original_call = self.test_object.get_dictionary('test_word')
        output = out.getvalue().strip()
        result = ("Examples of the word test_word are"
                  "\n* test1\n* test1\n* test1\nSynonyms of the word test_word"
                  " are\ntest1\ntest2\ntest3\ntest1\ntest2\ntest3\ntest1"
                  "\ntest2\ntest3\nNo Antonyms for the word test_word\n"
                  "Definitions of the word test_word are\ntest1\ntest1\ntest1")
        self.assertEqual(output, result)
        self.set_mock_and_test_antonyms(mock, instance)
        original_call = self.test_object.get_dictionary('test_word')
        output = out.getvalue().strip()
        result = ("Examples of the word test_word are"
                  "\n* test1\n* test1\n* test1\nSynonyms of the word test_word"
                  " are\ntest1\ntest2\ntest3\ntest1\ntest2\ntest3\ntest1"
                  "\ntest2\ntest3\nNo Antonyms for the word test_word\n"
                  "Definitions of the word test_word are\ntest1\ntest1\ntest1"
                  "\nExamples of the word test_word are\n* test1\n* test1\n*"
                  " test1\nNo Synonyms for the word test_word\nAntonyms of the"
                  " word test_word are\ntest1\ntest2\ntest1\ntest2\ntest1\n"
                  "test2\nDefinitions of the word test_word are\ntest1\ntest1"
                  "\ntest1")
        self.assertEqual(output, result)
        sys.stdout = saved_stdout

    def set_mock_and_test_antonyms(self, mock, method):
        mock.relationshipType = 'antonym'
        mock.words = ['test1', 'test2']
        method.getRelatedWords.return_value = [mock, mock, mock]
        original_call = self.test_object.get_antonyms('test')
        self.assertEqual(len(original_call), 6)
        result = ['test1', 'test2', 'test1', 'test2', 'test1', 'test2']
        self.assertEqual(result, original_call)
        return [mock, method]

    def set_mock_and_test_synonyms(self, mock, method):
        mock.relationshipType = "synonym"
        mock.words = ['Test1', 'Test2', 'Test3']
        method.getRelatedWords.return_value = [mock, mock, mock]
        original_call = self.test_object.get_synonyms('test')
        self.assertEqual(len(original_call), 9)
        result = ['test1', 'test2', 'test3',
                  'test1', 'test2', 'test3',
                  'test1', 'test2', 'test3']
        self.assertEqual(original_call, result)
        return [mock, method]

    def set_mock_and_test_definitions(self, mock, method):
        mock.text = 1
        method.getDefinitions.return_value = [mock, mock, mock]
        original_call = self.test_object.get_definitions(mock)
        self.assertEqual(len(method.getDefinitions()), len(original_call))
        self.assertEqual(original_call, [1, 1, 1])
        return [mock, method]

    def set_mock_and_test_examples(self, mock, method):
        mock.text = 'test1'
        method.getExamples.return_value = mock
        mock.examples = [mock, mock, mock]
        saved_stdout = sys.stdout
        out = StringIO()
        sys.stdout = out
        original_call = self.test_object.get_examples('test_word')
        output = out.getvalue().strip()
        result = ("Examples of the word test_word are\n* test1\n* test1\n*"
                  " test1")
        self.assertEqual(output, result)
        sys.stdout = saved_stdout
        return [mock, method]

if __name__ == '__main__':
    unittest.main()
