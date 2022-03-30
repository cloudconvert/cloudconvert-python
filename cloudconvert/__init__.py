from cloudconvert.cloudconvertrestclient import *
from cloudconvert.task import Task
from cloudconvert.job import Job
from cloudconvert.webhook import Webhook
from cloudconvert.signed_url import SignedUrl

def configure(**config):
    """
    Configure the REST Client With Latest API Key and Mode
    :return:
    """
    set_config(**config)


def default():
    """
    Configure the REST Client With Default API Key and Mode
    :return:
    """
    default_client()

