import os
from wordnik import *
import sys


class CommandLineDict(object):

    def __init__(self):
        apiUrl = 'http://api.wordnik.com/v4'
        apiKey = os.environ['API_KEY']
        self.client = swagger.ApiClient(apiKey, apiUrl)

    def get_definitions(self):
        pass


if __name__ == '__main__':
    class_object = CommandLineDict()   
    if sys.argv[1] == 'def':
        class_object.get_definitions()
