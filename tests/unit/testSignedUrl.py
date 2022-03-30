###################################################################
##      Test case for Signed URLs                                ##
##                                                               ##
## How to run ? :                                                ##
##                $ python testSignedUrl.py                      ##
###################################################################

import sys
import os
sys.path.append(os.getcwd())

import unittest
import cloudconvert



class TestSignedUrl(unittest.TestCase):

    def setUp(self):
        """
        Test case setup method
        :return:
        """
        print("Setting up signed URL test case")

    def testVerifySignature(self):
        """
        Test verify
        :return:
        """
        print("Testcase for creating signed URL..")

        # create dict for new Job
        job = {
            "tasks": {
                "import-file": {
                    "operation": "import/url",
                    "url": "https://github.com/cloudconvert/cloudconvert-php/raw/master/tests/Integration/files/input.pdf"
                },
                "export-file": {
                    "operation": "export/url",
                    "input": "import-file"
                }
            }
        }

        base = "https://s.cloudconvert.com/b3d85428-584e-4639-bc11-76b7dee9c109"
        signing_secret = "NT8dpJkttEyfSk3qlRgUJtvTkx64vhyX"
        cache_key = "mykey"

        url = cloudconvert.SignedUrl.sign(base, signing_secret, job, cache_key)

        print(url)

        self.assertIn("https://s.cloudconvert.com/", url)
        self.assertIn("?job=", url)
        self.assertIn("&cache_key=mykey", url)
        self.assertIn("&s=6dd147217a39534249a3cb418b357ba8cceacf74fc0db0d52630a07cac1ca268", url)



    def tearDown(self):
        """
        Teardown method
        :return:
        """
        print("Tearing down test case for signed URL..")


if __name__ == '__main__':
    unittest.main()
