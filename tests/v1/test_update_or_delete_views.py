from django.middleware.csrf import CsrfViewMiddleware
import pytest

from method_specific_views.v1.exceptions import RFC2616Violation
from method_specific_views.v1.views import UpdateOrDeleteResourceView
from tests.v1.dummy_project.dummy_app.views import DummyUpdateOrDeleteResourceView


@pytest.fixture
def update_or_delete_url():

    return '/update_or_delete/1/'


def test_sending_a_delete_to_an_update_or_delete_view_with_csrf_token_gets_accepted(delete_request):

    CsrfViewMiddleware().process_request(delete_request)
    CsrfViewMiddleware().process_view(delete_request, DummyUpdateOrDeleteResourceView.as_view(), (), {})
    assert delete_request.csrf_processing_done == True

def test_sending_a_delete_to_an_update_or_delete_view_without_csrf_token_returns_status_code_403(django_client,
                                                                                                 update_or_delete_url):

    """
    Ensure that an HTTP DELETE request without the proper headers and cookies is treated as unauthorized (403)
    """

    response = django_client.delete(update_or_delete_url)
    assert response.status_code == 403


def test_sending_a_delete_to_an_update_or_delete_view_that_has_not_implemented_delete_raises_not_implemented(delete_request):

    with pytest.raises(NotImplementedError):
        delete_response = CsrfViewMiddleware(UpdateOrDeleteResourceView().delete)(delete_request)


def test_sending_a_get_to_an_update_or_delete_view_that_has_not_implemented_get_raises_not_implemented(post_request):

    with pytest.raises(NotImplementedError):
        post_response = CsrfViewMiddleware(UpdateOrDeleteResourceView().get)(post_request)


@pytest.mark.django_db
def test_sending_a_patch_to_an_update_or_patch_view_with_csrf_token_gets_accepted(patch_request):

    CsrfViewMiddleware().process_request(patch_request)
    CsrfViewMiddleware().process_view(patch_request, DummyUpdateOrDeleteResourceView.as_view(), (), {})
    assert patch_request.csrf_processing_done == True


def test_sending_a_patch_to_an_update_or_patch_view_without_csrf_token_returns_status_code_403(django_client,
                                                                                               update_or_delete_url):

    """
    Ensure that an HTTP PATCH request without the proper headers and cookies is treated as unauthorized (403)
    """

    response = django_client.patch(update_or_delete_url)
    assert response.status_code == 403


def test_sending_a_patch_to_an_update_or_delete_view_that_has_not_implemented_patch_raises_not_implemented(patch_request):

    with pytest.raises(NotImplementedError):
        patch_response = CsrfViewMiddleware(UpdateOrDeleteResourceView().patch)(patch_request)


def test_sending_a_put_to_an_update_or_delete_view_with_csrf_token_gets_accepted(put_request,):

    CsrfViewMiddleware().process_request(put_request)
    CsrfViewMiddleware().process_view(put_request, DummyUpdateOrDeleteResourceView.as_view(), (), {})
    assert put_request.csrf_processing_done == True


def test_sending_a_head_to_an_update_or_delete_view_with_csrf_token_gets_accepted(head_request,):

    CsrfViewMiddleware().process_request(head_request)
    CsrfViewMiddleware().process_view(head_request, DummyUpdateOrDeleteResourceView.as_view(), (), {})
    assert head_request.csrf_processing_done == True


def test_sending_a_put_to_an_update_or_delete_view_without_csrf_token_returns_status_code_403(django_client,
                                                                                              update_or_delete_url):

    """
    Ensure that an HTTP PUT request without the proper headers and cookies is treated as unauthorized (403)
    """

    response = django_client.put(update_or_delete_url)
    assert response.status_code == 403


def test_sending_a_put_to_an_update_or_delete_view_that_has_not_implemented_putt_raises_not_implemented(put_request):


    with pytest.raises(NotImplementedError):
        put_response = CsrfViewMiddleware(UpdateOrDeleteResourceView().put)(put_request)


def test_using_an_update_or_delete_view_to_serve_post_requests_raises_rfc2616violation(client,
                                                                                      update_or_delete_url):
    """
    Ensure that POST requests are not served through UpdateOrDeleteResourceView subclasses.

    ! Pay attention to the point that pytest's `client` fixture is used here instead of
    our own `django_client` fixture, since we're no longer validating the CSRF processing
    """

    with pytest.raises(RFC2616Violation):
        client.post(update_or_delete_url)
