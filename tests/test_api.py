

import unittest
import os


from cloudconvert.api import Api
from cloudconvert.process import Process
from cloudconvert.exceptions import (
    APIError, HTTPError, BadRequest, ConversionFailed, TemporaryUnavailable, InvalidResponse, InvalidParameterException
)


class testApi(unittest.TestCase):

    ## test helpers

    def setUp(self):
        self.api = Api(api_key=os.environ.get('API_KEY'))

    def tearDown(self):
        self.api = None

    def test_01_if_request_without_auth_works(self):
        response = self.api.get("/conversiontypes", {
            'inputformat': 'pdf',
            'outputformat': 'jpg'
        }, False)
        self.assertIsNotNone(response)


    def test_02_if_request_with_auth_works(self):
        response = self.api.post("/process", {
            'inputformat': 'pdf',
            'outputformat': 'jpg'
        }, True)
        self.assertIsNotNone(response)


    def test_03_if_process_creation_works(self):
        process = self.api.createProcess({
            'inputformat': 'pdf',
            'outputformat': 'jpg'
        })
        self.assertIsInstance(process, Process)


    def test_04_if_process_creation_with_invalid_format_throws_the_right_exception(self):
        with self.assertRaises(BadRequest):
            self.api.createProcess({
                'inputformat': 'invalid',
                'outputformat': 'jpg'
            })


