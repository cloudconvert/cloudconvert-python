###################################################################
##      Test case for Webhook signature                          ##
##                                                               ##
## How to run ? :                                                ##
##                $ python testWebhookSignature.py               ##
###################################################################

import sys
import os
sys.path.append(os.getcwd())

import unittest
import cloudconvert


# Set webhook signature
WEBHOOK_SIGNATURE = "5c4c0691bce8a1a2af738b7073fe0627e792734813358c5f88a658819dd0a6d2"


class TestWebhookSignature(unittest.TestCase):

    def setUp(self):
        """
        Test case setup method
        :return:
        """
        print("Setting up webhook signature test case")

    def testVerifySignature(self):
        """
        Test verify
        :return:
        """
        print("Testcase for verifying signature..")
        verified = cloudconvert.Webhook.verify("cloudconvert", WEBHOOK_SIGNATURE, "90sffs0d8fs0f9sf0")

        assert verified == True, "Signature did not match"

    def tearDown(self):
        """
        Teardown method
        :return:
        """
        print("Tearing down test case for webhook signature..")


if __name__ == '__main__':
    unittest.main()
