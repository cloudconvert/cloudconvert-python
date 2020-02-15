import uuid
import urllib
import cloudconvert.utils as util
from cloudconvert.cloudconvertrestclient import default_client


class Resource(object):
    """Base class for all REST services
    """
    convert_resources = {}

    def __init__(self, attributes=None, api_client=None):
        attributes = attributes or {}
        self.__dict__['api_client'] = api_client or default_client()

        super(Resource, self).__setattr__('__data__', {})
        super(Resource, self).__setattr__('error', None)
        super(Resource, self).__setattr__('headers', {})
        super(Resource, self).__setattr__('header', {})
        super(Resource, self).__setattr__('request_id', None)
        self.merge(attributes)

    def generate_request_id(self):
        """Generate uniq request id
        """
        if self.request_id is None:
            self.request_id = str(uuid.uuid4())
        return self.request_id

    def http_headers(self):
        """Generate HTTP header
        """
        return util.merge_dict(self.header, self.headers,
                               {'CloudConvert-Request-Id': self.generate_request_id()})

    def __str__(self):
        return self.__data__.__str__()

    def __repr__(self):
        return self.__data__.__str__()

    def __getattr__(self, name):
        return self.__data__.get(name)

    def __setattr__(self, name, value):
        try:
            # Handle attributes(error, header, request_id)
            super(Resource, self).__getattribute__(name)
            super(Resource, self).__setattr__(name, value)
        except AttributeError:
            self.__data__[name] = self.convert(name, value)

    def __contains__(self, item):
        return item in self.__data__

    def success(self):
        return self.error is None

    def merge(self, new_attributes):
        """Merge new attributes e.g. response from a post to Resource
        """
        for k, v in new_attributes.items():
            setattr(self, k, v)

    def convert(self, name, value):
        """Convert the attribute values to configured class
        """
        if isinstance(value, dict):
            cls = self.convert_resources.get(name, Resource)
            return cls(value, api_client=self.api_client)
        elif isinstance(value, list):
            new_list = []
            for obj in value:
                new_list.append(self.convert(name, obj))
            return new_list
        else:
            return value

    def __getitem__(self, key):
        return self.__data__[key]

    def __setitem__(self, key, value):
        self.__data__[key] = self.convert(key, value)

    def to_dict(self):

        def parse_object(value):
            if isinstance(value, Resource):
                return value.to_dict()
            elif isinstance(value, list):
                return list(map(parse_object, value))
            else:
                return value

        return dict((key, parse_object(value)) for (key, value) in self.__data__.items())

    def to_json(self):

        def parse_object(value):
            if isinstance(value, Resource):
                return value.to_dict()
            elif isinstance(value, list):
                return list(map(parse_object, value))
            else:
                return value

        return dict((key, parse_object(value)) for (key, value) in self.__data__.items())


class Find(Resource):
    @classmethod
    def find(cls, id):
        """Locate resource e.g. job with given id
        Usage::
            >>> job = Job.find("s9fsf9-s9f9sf9s-ggfgf9-fg9fg")
        """
        api_client = default_client()

        url = util.join_url(cls.path, str(id))
        res = api_client.get(url)
        try:
            return res["data"]
        except:
            return res


class List(Resource):
    list_class = Resource

    @classmethod
    def all(cls, params=None):
        """Get list of payments as on
        https://cloudconvert.com/api/v2/tasks#tasks-list
        Usage::
            >>> tasks_list = tasks.all({'status': 'waiting'})
        """
        api_client = default_client()

        if params is None:
            url = cls.path
        else:
            url = util.join_url_params(cls.path, params)

        try:
            response = api_client.get(url)
            res = cls.list_class(response, api_client=api_client)
            try:
                return res.to_json().get("data")
            except:
                return res.to_json()
        except AttributeError:
            # To handle the case when response is JSON Array
            if isinstance(response, list):
                new_resp = [cls.list_class(elem, api_client=api_client) for elem in response]
                return new_resp


class Create(Resource):

    @classmethod
    def create(cls, operation=None, payload={}):
        """Creates a resource e.g. task
        Usage::
            >>> task = Task({})
            >>> task.create(name=TASK_NAME) # return newly created task
        """

        api_client = default_client()
        url = util.join_url('v2', operation or '')
        res = api_client.post(url, payload, headers={})

        try:
            return res["data"]
        except:
            return res


class Wait(Resource):
    @classmethod
    def wait(cls, id):
        """Wait resource e.g. job with given id
        Usage::
            >>> job = job.wait("s9fsf9-s9f9sf9s-ggfgf9-fg9fg")
        """
        api_client = default_client()

        url = util.join_url(cls.path, str(id), "wait")
        res = api_client.get(url)
        try:
            return res["data"]
        except:
            return res


class Show(Resource):
    @classmethod
    def show(cls, id):
        """show resource e.g. job with given id
        Usage::
            >>> job = Job.show("s9fsf9-s9f9sf9s-ggfgf9-fg9fg")
        """
        api_client = default_client()
        url = util.join_url(cls.path, str(id))
        res = api_client.get(url)
        try:
            return res["data"]
        except:
            return res


class Delete(Resource):
    @classmethod
    def delete(cls, id):
        """Deletes a resource e.g. task
        Usage::
            >>> Task.delete(TASK_ID)
        """
        api_client = default_client()
        url = util.join_url(cls.path, str(id))
        api_resource = Resource()
        new_attributes = api_client.delete(url)
        api_resource.error = None
        api_resource.merge(new_attributes)
        return api_resource.success()
