###################################################################
##      Test cases for Cloud Convert API tasks endpoints         ##
##                                                               ##
## How to run ? :                                                ##
##                $ python tests/unit/testTask.py                ##
###################################################################

import sys
import os
sys.path.append(os.getcwd())

import unittest
import requests_mock
import cloudconvert
import json
from cloudconvert.config import SANDBOX_API_KEY


class TaskTestCase(unittest.TestCase):

    def setUp(self):
        """
        Test case setup method
        :return:
        """
        print("Setting up Task test cases")
        self.cloudconvert = cloudconvert

        # setup the client with the provided API key by configuring
        self.cloudconvert.configure(api_key = SANDBOX_API_KEY, sandbox = True)
        self.responses_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "responses")

    def testCreateTask(self):
        """
        Create Task
        :return:
        """
        print("testcase for creating task..")

        # create dict for new task
        new_import_url_task = {
            "url": "https://github.com/cloudconvert/cloudconvert-php/raw/master/tests/Integration/files/input.pdf"
        }

        with requests_mock.mock() as m:
            with open("{}/{}".format(self.responses_path, "task_created.json")) as f:
                response_json = json.load(f)

            m.post("https://api.sandbox.cloudconvert.com/v2/import/url", json=response_json)
            task = self.cloudconvert.Task.create(operation="import/url", payload=new_import_url_task)

            self.assertEqual(first=task['id'], second="2f901289-c9fe-4c89-9c4b-98be526bdfbf")
            print(m.called)

    def testWaitTask(self):
        """
        Wait Task
        :return:
        """
        print("testcase for waiting task..")

        with requests_mock.mock() as m:
            with open("{}/{}".format(self.responses_path, "task.json")) as f:
                response_json = json.load(f)

            task_id = "4c80f1ae-5b3a-43d5-bb58-1a5c4eb4e46b"
            m.get("https://api.sandbox.cloudconvert.com/v2/tasks/{}/wait".format(task_id), json=response_json)

            task = self.cloudconvert.Task.wait(id=task_id)

            self.assertEqual(first=task['id'], second="4c80f1ae-5b3a-43d5-bb58-1a5c4eb4e46b")
            print(m.called)

    def testShowTask(self):
        """
        Show Task
        :return:
        """
        print("testcase for show task..")

        with requests_mock.mock() as m:
            with open("{}/{}".format(self.responses_path, "task.json")) as f:
                response_json = json.load(f)

            task_id = "4c80f1ae-5b3a-43d5-bb58-1a5c4eb4e46b"
            m.get("https://api.sandbox.cloudconvert.com/v2/tasks/{}".format(task_id), json=response_json)

            task = self.cloudconvert.Task.show(id=task_id)

            self.assertEqual(first=task['id'], second="4c80f1ae-5b3a-43d5-bb58-1a5c4eb4e46b")
            print(m.called)

    def testListTask(self):
        """
        List Task
        :return:
        """
        print("testcase for listing tasks..")

        with requests_mock.mock() as m:
            with open("{}/{}".format(self.responses_path, "tasks.json")) as f:
                response_json = json.load(f)

            m.get("https://api.sandbox.cloudconvert.com/v2/tasks", json=response_json)
            tasks = self.cloudconvert.Task.all()

            self.assertEqual(isinstance(tasks, list), True)
            print(m.called)

    def testRetryTask(self):
        """
        Retry Task
        :return:
        """
        print("testcase for retrying a task")
        with requests_mock.mock() as m:
            with open("{}/{}".format(self.responses_path, "retry.json")) as f:
                response_json = json.load(f)

            task_id = "66bd538e-1500-4e4b-b908-0e429b357e77"
            m.post("https://api.sandbox.cloudconvert.com/v2/tasks/{}/retry".format(task_id), json=response_json)
            tasks = self.cloudconvert.Task.retry(task_id)

            self.assertEqual(tasks["retry_of_task_id"], task_id)
            print(m.called)

    def testDeleteTask(self):
        """
        Delete Task
        :return:
        """
        print("testcase for delete task..")

        with requests_mock.mock() as m:

            task_id = "4c80f1ae-5b3a-43d5-bb58-1a5c4eb4e46b"
            m.delete("https://api.sandbox.cloudconvert.com/v2/tasks/{}".format(task_id), json={})

            isDeleted = self.cloudconvert.Task.delete(id=task_id)
            self.assertEqual(first=isDeleted, second=True)
            print(m.called)

    def testDownloadOutput(self):
        """
        Testcase to download output file
        :return:
        """
        res = cloudconvert.download(filename="path/to/save/file.ext", url="url/to/file/download")
        print(res)

    def tearDown(self):
        """
        Teardown method
        :return:
        """
        print("Tearing down task test cases..")



if __name__ == '__main__':
    unittest.main()
