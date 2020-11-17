import os

import django
from django.conf import settings
from django.http import HttpRequest
from django.test.client import Client
import pytest

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.v1.dummy_project.dummy_project.settings'
django.setup()

class ShallowHttpRequest(HttpRequest):

    """
    A version of HttpRequest that allows us to change some things
    more easily
    """

    def __init__(self):
        super().__init__()
        # A real session backend isn't needed.
        self.session = {}

    def is_secure(self):
        return getattr(self, '_is_secure_override', False)


@pytest.fixture
def http_request(django_client):

    http_request = ShallowHttpRequest()
    response = django_client.get('/give_me_a_csrf_token/')

    http_request.COOKIES[settings.CSRF_COOKIE_NAME] = response.cookies[settings.CSRF_COOKIE_NAME].coded_value
    http_request.META['HTTP_X_CSRFTOKEN'] = str(response.context['csrf_token'])

    return http_request


@pytest.fixture
def delete_request(http_request):

    http_request.method = "DELETE"
    return http_request


@pytest.fixture
def patch_request(http_request):

    http_request.method = "PATCH"
    return http_request


@pytest.fixture
def post_request(http_request):

    http_request.method = "POST"
    return http_request


@pytest.fixture
def put_request(http_request):

    http_request.method = "PUT"
    return http_request


@pytest.fixture
def head_request(http_request):

    http_request.method = "HEAD"
    return http_request


@pytest.fixture
def django_client():
    """
    By default, Django's test client disables CRSF token validation

    https://docs.djangoproject.com/en/2.0/ref/csrf/#testing
    """

    return Client(enforce_csrf_checks=True)
