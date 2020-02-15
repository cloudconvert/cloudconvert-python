from cloudconvert.resource import List, Find, Delete, Wait, Show, Create


class Job(List, Find, Wait, Show, Delete):
    """Job class wrapping the REST v2/jobs endpoint. Enabling New Job Creation, Showing a job, Waiting for job,
    Finding a job, Deleting a job.

    Usage::
        >>> jobs = Job.list({"page": 5})
        >>> job = Job.find("<Job_ID>")
        >>> Job.create()
        >>> Job.delete()<Job_ID>)     # return True or False
    """
    path = "v2/jobs"

    @classmethod
    def create(cls, payload={}):
        res = Create.create(operation="jobs", payload=payload)
        try:
            return res['data']
        except:
            return res


Job.convert_resources['jobs'] = Job
Job.convert_resources['job'] = Job

