

import unittest
import os


from cloudconvert.api import Api
from cloudconvert.process import Process
from cloudconvert.exceptions import (
    APIError, HTTPError, BadRequest, ConversionFailed, TemporaryUnavailable, InvalidResponse, InvalidParameterException
)


class testProcess(unittest.TestCase):

    ## test helpers

    def setUp(self):
        self.api = Api(api_key=os.environ.get('API_KEY'))

    def tearDown(self):
        self.api = None



    def test_01_if_process_with_input_download_works(self):
        process = self.api.createProcess({
            'inputformat': 'png',
            'outputformat': 'jpg'
        })
        process.start({
            'input': 'download',
            'outputformat': 'jpg',
            'wait': True,
            'file': 'https://cloudconvert.com/blog/wp-content/themes/cloudconvert/img/logo_96x60.png'
        })
        self.assertEqual(process['step'],'finished')
        self.assertEqual(process['output']['ext'],'jpg')

        ## cleanup
        process.delete()



    def test_02_if_process_with_input_upload_works(self):
        process = self.api.createProcess({
            'inputformat': 'png',
            'outputformat': 'jpg'
        })
        process.start({
            'input': 'upload',
            'outputformat': 'jpg',
            'wait': True,
            'file': open('input.png', 'rb')
        })
        self.assertEqual(process['step'],'finished')
        self.assertEqual(process['output']['ext'],'jpg')

        ## cleanup
        process.delete()



    def test_03_if_process_with_input_upload_and_custom_options_works(self):
        process = self.api.createProcess({
            'inputformat': 'png',
            'outputformat': 'jpg'
        })
        process.start({
            'input': 'upload',
            'outputformat': 'jpg',
            'wait': True,
            'file': open('input.png', 'rb'),
            'converteroptions': {
                'quality': 10
            }
        })
        self.assertEqual(process['step'],'finished')
        self.assertEqual(process['output']['ext'],'jpg')
        self.assertEqual(int(process['converter']['options']['quality']),10)

        ## cleanup
        process.delete()



    def test_04_if_download_of_output_file_works(self):
        process = self.api.createProcess({
            'inputformat': 'png',
            'outputformat': 'pdf'
        })
        process.start({
            'input': 'upload',
            'outputformat': 'pdf',
            'file': open('input.png', 'rb')
        })
        process.wait()
        process.download("output.pdf")
        self.assertTrue(os.path.isfile("output.pdf"))

        ## cleanup
        os.remove("output.pdf")
        process.delete()



    def test_05_if_download_of_multiple_output_file_works(self):
        process = self.api.createProcess({
            'inputformat': 'pdf',
            'outputformat': 'jpg'
        })
        process.start({
            'input': 'upload',
            'outputformat': 'jpg',
            'file': open('input.pdf', 'rb'),
            'converteroptions': {
                'page_range': '1-2'
            }
        })
        process.wait()
        process.downloadAll()
        self.assertTrue(os.path.isfile("input-0.jpg"))
        self.assertTrue(os.path.isfile("input-1.jpg"))

        ## cleanup
        os.remove("input-0.jpg")
        os.remove("input-1.jpg")
        process.delete()



    def test_06_if_convert_shortcut_works(self):
        process = self.api.convert({
            'inputformat': 'png',
            'outputformat': 'jpg',
            'input': 'upload',
            'file': open('input.png', 'rb')
        }).wait()
        self.assertEqual(process['step'],'finished')
        self.assertEqual(process['output']['ext'],'jpg')

        ## cleanup
        process.delete()
