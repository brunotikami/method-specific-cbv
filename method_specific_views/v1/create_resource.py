from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import requires_csrf_token

from method_specific_views.v1.exceptions import RFC2616Violation


HTTP_METHODS_THAT_SHOULD_NOT_CREATE_RESOURCES  = ['DELETE', 'OPTIONS', 'PUT', 'PATCH', 'TRACE']

@method_decorator(ensure_csrf_cookie, name="get")
@method_decorator(requires_csrf_token, name="post")
class CreateResourceView(View):

    """
    This base class-based view aims to ensure that 
    GET requests always get CSRF tokens set and that
    POST requests are always wrapped with a 
    `requires_csrf_token` decorator to ensure 
    that no data is manipulated without 
    the usage of CSRF tokens.
    """


    def __getattribute__(self, item):

        type_of_object_is_a_subclass = issubclass(type(self), CreateResourceView)

        http_method_should_not_create_resources = item.upper() in HTTP_METHODS_THAT_SHOULD_NOT_CREATE_RESOURCES

        if type_of_object_is_a_subclass and http_method_should_not_create_resources: 

            msg = _('Don\'t use {} to create a resource. Use <UpdateOrDeleteResourceView> instead.'.format(item))
            raise RFC2616Violation(msg)

        return super().__getattribute__(item)

    def get(self, request, *args, **kwargs):

        raise NotImplementedError()

    def post(self, request, *args, **kwargs):

        raise NotImplementedError()

