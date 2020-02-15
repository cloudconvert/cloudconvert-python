from __future__ import division

import datetime
import requests
import json
import logging
import os
import platform
import ssl
import urllib

import cloudconvert.utils as util
from cloudconvert.exceptions import exceptions
from cloudconvert.config import __version__, __endpoint_map__

log = logging.getLogger(__name__)


class CloudConvertRestClient(object):
    # User-Agent for HTTP request
    ssl_version = "" if util.older_than_27() else ssl.OPENSSL_VERSION
    ssl_version_info = None if util.older_than_27() else ssl.OPENSSL_VERSION_INFO
    library_details = "requests %s; python %s; %s" % (
        requests.__version__, platform.python_version(), ssl_version)
    user_agent = "CloudConvertSDK/CloudConvert-Python-SDK %s (%s)" % (
        __version__, library_details)

    def __init__(self, options=None, **kwargs):
        """Create Client object
        Usage::
            >>> import cloudconvert.cloudconvertrestclient as cloudconvertrestclient
            >>> rest_client = cloudconvertrestclient.CloudConvertRestClient(token='access_token', ssl_options={"cert": "/path/to/server.pem"})
        """
        kwargs = util.merge_dict(options or {}, kwargs)

        self.mode = 'sandbox' if kwargs.get("sandbox", False) else 'live'

        if self.mode != "live" and self.mode != "sandbox":
            raise exceptions.InvalidConfig("Configuration Mode Invalid", "Received: %s" % (self.mode),
                                           "Required: live or sandbox")

        self.endpoint = kwargs.get("endpoint", self.default_endpoint())
        # Mandatory parameter, so not using `dict.get`
        self.proxies = kwargs.get("proxies", None)
        self.token_hash = None
        # setup SSL certificate verification if private certificate provided
        ssl_options = kwargs.get("ssl_options", {})
        if "cert" in ssl_options:
            os.environ["REQUESTS_CA_BUNDLE"] = ssl_options["cert"]

        if kwargs.get("api_key"):
            self.token_hash = {
                "access_token": kwargs["api_key"], "token_type": "Bearer"}

        self.options = kwargs

    def default_endpoint(self):
        return __endpoint_map__.get(self.mode)

    def request(self, url, method, body=None, headers=None):
        """Make HTTP call, formats response and does error handling. Uses http_call method in CloudConvertRestClient class.
        Usage::
            >>> cloudconvertrestclient.request("https://api.sandbox.cloudconvert.com/v2/jobs/JOB-ID", "GET", {})
            >>> cloudconvertrestclient.request("https://api.sandbox.cloudconvert.com/v2/tasks/TASK-ID", "POST", "{}", {} )
        """

        http_headers = util.merge_dict(
            self.headers(), headers or {})

        try:
            return self.http_call(url, method, json=body, headers=http_headers)

        # Format Error message for bad request
        except exceptions.BadRequest as error:
            return {"error": json.loads(error.content)}

        # Handle Expired token
        except exceptions.UnauthorizedAccess as error:
            if self.token_hash:
                self.token_hash = None
                return self.request(url, method, body, headers)
            else:
                raise error

    def http_call(self, url, method, **kwargs):
        """Makes a http call. Logs response information.
        """
        log.info('Request[%s]: %s' % (method, url))

        if self.mode.lower() != 'live':
            request_headers = kwargs.get("headers", {})
            request_body = kwargs.get("json", {})
            log.debug("Level: " + self.mode)
            log.debug('Request: \nHeaders: %s\nBody: %s' % (
                str(request_headers), str(request_body)))
        else:
            log.info(
                'Not logging full request/response headers and body in live mode for compliance')

        start_time = datetime.datetime.now()
        response = requests.request(
            method, url, proxies=self.proxies, **kwargs)

        duration = datetime.datetime.now() - start_time
        log.info('Response[%d]: %s, Duration: %s.%ss.' % (
            response.status_code, response.reason, duration.seconds, duration.microseconds))

        if self.mode.lower() != 'live':
            log.debug('Headers: %s\nBody: %s' % (
                str(response.headers), str(response.content)))

        return self.handle_response(response, response.content.decode('utf-8'))

    def handle_response(self, response, content):
        """Validate HTTP response
        """
        status = response.status_code
        if status in (301, 302, 303, 307):
            raise exceptions.Redirection(response, content)
        elif 200 <= status <= 299:
            return json.loads(content) if content else {}
        elif status == 400:
            raise exceptions.BadRequest(response, content)
        elif status == 401:
            return json.loads(content) if content else {}
        elif status == 403:
            raise exceptions.ForbiddenAccess(response, content)
        elif status == 404:
            return json.loads(content) if content else {}
        elif status == 405:
            raise exceptions.MethodNotAllowed(response, content)
        elif status == 409:
            raise exceptions.ResourceConflict(response, content)
        elif status == 410:
            raise exceptions.ResourceGone(response, content)
        elif status == 422:
            raise exceptions.ResourceInvalid(response, content)
        elif 401 <= status <= 499:
            raise exceptions.ClientError(response, content)
        elif 500 <= status <= 599:
            raise exceptions.ServerError(response, content)
        else:
            raise exceptions.ConnectionError(
                response, content, "Unknown response code: #{response.code}")

    def headers(self):
        """Default HTTP headers
        """
        return {
            "Authorization": ("%s %s" % (self.token_hash['token_type'], self.token_hash['access_token'])),
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": self.user_agent
        }

    def get(self, action, headers=None):
        """Make GET request
        Usage::
            >>> cloudconvertrestclient.get("v2/tasks/TASK-ID")
            >>> cloudconvertrestclient.get("v2/jobs/JOB-ID")
        """
        return self.request(util.join_url(self.endpoint, action), 'GET', headers=headers or {})

    def post(self, action, params=None, headers={}):
        """Make POST request
        Usage::
            >>> cloudconvertrestclient.post("v2/jobs/", {"tasks": {
                                                "task-import-file7": {
                                                    "operation": "import/url",
                                                    "url": "https://file-examples.com/wp-content/uploads/2017/02/"
                                                   }}})
            >>> cloudconvertrestclient.post("v2/export/url",  {
                                                    "input": "f1e276cf-1cfa-4cd5-8c87-1e3d07206cf3",
                                                    "file": "file-sample_100kB.doc"})
        """

        return self.request(util.join_url(self.endpoint, action), 'POST', body=params or {}, headers={} or headers)

    def put(self, action, params=None, headers=None):
        """Make PUT request
        """
        return self.request(util.join_url(self.endpoint, action), 'PUT', body=params or {}, headers=headers or {})

    def patch(self, action, params=None, headers=None):
        """Make PATCH request
        Usage::
        """
        return self.request(util.join_url(self.endpoint, action), 'PATCH', body=params or {}, headers=headers or {})

    def delete(self, action, headers=None):
        """Make DELETE request
        """
        return self.request(util.join_url(self.endpoint, action), 'DELETE', headers=headers or {})


__client__ = None


def download(url, filename):
    """Download a file  e.g. from a given url
    Usage::
        >>> cloudconvert.download(url="https://exported_url", filename="sample.pdf")
    """
    try:
        urllib.request.urlretrieve(url, filename)
        print("Downloaded file:{} successfully..".format(filename))
        return filename
    except Exception as e:
        print("Got exception while trying to download the file from url: {}".format(url))
        print(e)

    return None


def default_client():
    """Returns default api object and if not present creates a new one
    By default points to developer sandbox
    """
    from cloudconvert.environment_vars import CLOUDCONVERT_API_KEY
    global __client__
    if __client__ is None:
        try:
            API_KEY = os.environ[CLOUDCONVERT_API_KEY]
        except KeyError:
            raise exceptions.MissingConfig(
                "Required CLOUDCONVERT_API_KEY \n Refer https://cloudconvert.com/api/v2#overview")

        # Get default API mode
        sandbox = True if os.environ.get("CLOUDCONVERT_SANDBOX", "false") == 'true' else False

        __client__ = CloudConvertRestClient({}, sandbox=sandbox, api_key=API_KEY)

    return __client__


def set_config(options=None, **config):
    """Create new default api object with given configuration
    """
    global __client__
    __client__ = CloudConvertRestClient(options or {}, **config)
    return __client__
