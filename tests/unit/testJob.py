###################################################################
##      Test cases for Cloud Convert API jobs endpoints          ##
##                                                               ##
## How to run ? :                                                ##
##                $ python tests/unit/testJob.py                 ##
###################################################################

import sys
import os

sys.path.append(os.getcwd())

import unittest
import cloudconvert
import requests_mock
import json
from cloudconvert.config import SANDBOX_API_KEY


class JobTestCase(unittest.TestCase):

    def setUp(self):
        """
        Test case setup method
        :return:
        """
        print("Setting up Job test cases")
        self.cloudconvert = cloudconvert

        # setup the client with the provided API key by configuring
        self.cloudconvert.configure(api_key=SANDBOX_API_KEY, sandbox=True)
        self.responses_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "responses")

    def testCreateJob(self):
        """
        Create Job
        :return:
        """
        print("testcase for creating Job..")

        # create dict for new Job
        job_with_single_task = {
            "tasks": {
                "sandbox-task-import-file": {
                    "operation": "import/url",
                    "url": "https://github.com/cloudconvert/cloudconvert-php/raw/master/tests/Integration/files/input.pdf"
                }
            }
        }

        with requests_mock.mock() as m:
            with open("{}/{}".format(self.responses_path, "job_created.json")) as f:
                response_json = json.load(f)

            m.post("https://api.sandbox.cloudconvert.com/v2/jobs", json=response_json)
            job = self.cloudconvert.Job.create(payload=job_with_single_task)

            self.assertEqual(first=job['id'], second="5da371b0-0e43-41c4-94a1-1e04de2d2e29")
            print(m.called)

    def testWaitJob(self):
        """
        Wait Job
        :return:
        """
        print("testcase for waiting job..")

        with requests_mock.mock() as m:
            with open("{}/{}".format(self.responses_path, "job.json")) as f:
                response_json = json.load(f)

            job_id = "4c80f1ae-5b3a-43d5-bb58-1a5c4eb4e46b"
            m.get("https://api.sandbox.cloudconvert.com/v2/jobs/{}/wait".format(job_id), json=response_json)

            job = self.cloudconvert.Job.wait(id=job_id)

            self.assertEqual(first=job['id'], second="cd82535b-0614-4b23-bbba-b24ab0e892f7")
            print(m.called)

    def testShowJob(self):
        """
        Show Job
        :return:
        """
        print("testcase for show job..")

        with requests_mock.mock() as m:
            with open("{}/{}".format(self.responses_path, "job.json")) as f:
                response_json = json.load(f)

            job_id = "4c80f1ae-5b3a-43d5-bb58-1a5c4eb4e46b"
            m.get("https://api.sandbox.cloudconvert.com/v2/jobs/{}".format(job_id), json=response_json)

            job = self.cloudconvert.Job.show(id=job_id)

            self.assertEqual(first=job['id'], second="cd82535b-0614-4b23-bbba-b24ab0e892f7")
            print(m.called)

    def testListJob(self):
        """
        List Jobs
        :return:
        """
        print("testcase for listing Jobs..")

        with requests_mock.mock() as m:
            with open("{}/{}".format(self.responses_path, "jobs.json")) as f:
                response_json = json.load(f)

            m.get("https://api.sandbox.cloudconvert.com/v2/jobs", json=response_json)
            jobs = self.cloudconvert.Job.all()

            self.assertEqual(isinstance(jobs, list), True)
            print(m.called)

    def testDeleteJob(self):
        """
        Delete Job
        :return:
        """
        print("testcase for delete job..")

        with requests_mock.mock() as m:
            job_id = "66681017-2e84-4956-991f-d6513f6a4e35"
            m.delete("https://api.sandbox.cloudconvert.com/v2/jobs/{}".format(job_id), json={})

            isDeleted = self.cloudconvert.Job.delete(id=job_id)
            self.assertEqual(first=isDeleted, second=True)
            print(m.called)

    def tearDown(self):
        """
        Teardown method
        :return:
        """
        print("Tearing down job test cases..")


if __name__ == '__main__':
    unittest.main()
