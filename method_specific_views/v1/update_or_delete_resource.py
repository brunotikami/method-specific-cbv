from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import requires_csrf_token

from method_specific_views.v1.exceptions import RFC2616Violation


HTTP_METHODS_THAT_SHOULD_NOT_UPDATE_NOR_DELETE_RESOURCES  = ['OPTIONS', 'POST', 'TRACE']

@method_decorator(requires_csrf_token, name="delete")
@method_decorator(ensure_csrf_cookie, name="get")
@method_decorator(requires_csrf_token, name="patch")
@method_decorator(requires_csrf_token, name="put")
class UpdateOrDeleteResourceView(View):

    """
    This base class-based view aims to ensure that 
    DELETE, PATCH and PUT requests are always
    wrappedi with a `requires_csrf_token` decorator 
    to ensure that no data is manipulated without 
    the usage of CSRF tokens.
    """


    def __getattribute__(self, item):

        type_of_object_is_a_subclass = issubclass(type(self), UpdateOrDeleteResourceView)

        http_method_should_not_update_nor_delete_resources = False

        if item.upper() in HTTP_METHODS_THAT_SHOULD_NOT_UPDATE_NOR_DELETE_RESOURCES:
            http_method_should_not_update_nor_delete_resources = True

        if type_of_object_is_a_subclass and http_method_should_not_update_nor_delete_resources: 

            msg = 'Don\'t use {} to update or delete a resource. Use Django\'s <View> or <CreateResourceView> instead.'
            msg = _(msg.format(item.upper()))
            raise RFC2616Violation(msg)

        return super().__getattribute__(item)

    def delete(self, request, *args, **kwargs):

        raise NotImplementedError() 

    def get(self, request, *args, **kwargs):

        raise NotImplementedError()

    def patch(self, request, *args, **kwargs):

        raise NotImplementedError()

    def put(self, request, *args, **kwargs):

        raise NotImplementedError()
