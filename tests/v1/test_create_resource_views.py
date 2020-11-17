from django.middleware.csrf import CsrfViewMiddleware
import pytest

from method_specific_views.v1.exceptions import RFC2616Violation
from method_specific_views.v1.views import CreateResourceView
from tests.v1.dummy_project.dummy_app.views import DummyCreateResourceView


@pytest.fixture
def create_url():

    return '/create/1/'


@pytest.mark.django_db
def test_sending_a_post_to_a_create_view_with_csrf_token_gets_accepted(post_request):

    CsrfViewMiddleware().process_request(post_request)
    CsrfViewMiddleware().process_view(post_request, DummyCreateResourceView.as_view(), (), {})
    assert post_request.csrf_processing_done == True


def test_sending_a_head_to_a_create_view_with_csrf_token_gets_accepted(head_request):

    CsrfViewMiddleware().process_request(head_request)
    CsrfViewMiddleware().process_view(head_request, DummyCreateResourceView.as_view(), (), {})
    assert head_request.csrf_processing_done == True


def test_sending_a_post_to_a_create_view_without_csrf_token_returns_status_code_403(django_client,
                                                                                    create_url):

    """
    Ensure that an HTTP post request without the proper headers and cookies is treated as unauthorized (403)
    """

    response = django_client.post(create_url)
    assert response.status_code == 403


def test_sending_a_get_to_a_create_view_that_has_not_implemented_get_raises_not_implemented(post_request):

    with pytest.raises(NotImplementedError):
        post_response = CsrfViewMiddleware(CreateResourceView().get)(post_request)


def test_sending_a_post_to_a_create_view_that_has_not_implemented_post_raises_not_implemented(post_request):

    with pytest.raises(NotImplementedError):
        post_response = CsrfViewMiddleware(CreateResourceView().post)(post_request)



def test_using_a_create_resource_view_to_serve_update_methods_raises_rfc2616violation(client,
                                                                                      create_url):

    """
    Ensure that read methods are not served through CreateResourceView subclasses.

    ! Pay attention to the point that pytest's `client` fixture is used here instead of
    our own `django_client` fixture, since we're no longer validating the CSRF processing
    """

    with pytest.raises(RFC2616Violation):
        client.put(create_url)


def test_using_a_create_resource_view_to_serve_delete_requests_raises_rfc2616violation(client,
                                                                                       create_url):

    """
    Ensure that DELETE requests are not served through CreateResourceView subclasses.

    ! Pay attention to the point that pytest's `client` fixture is used here instead of
    our own `django_client` fixture, since we're no longer validating the CSRF processing
    """
    with pytest.raises(RFC2616Violation):
        client.delete(create_url)
