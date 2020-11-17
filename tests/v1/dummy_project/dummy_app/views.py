from django.http import HttpResponse
from django.template import engines
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

from method_specific_views.v1.views import CreateResourceView
from method_specific_views.v1.views import UpdateOrDeleteResourceView


@method_decorator(ensure_csrf_cookie, name="get")
class DummyCreateResourceView(CreateResourceView):

    def post(self, request, pk):

        return HttpResponse("POST OK")

class DummyUpdateOrDeleteResourceView(UpdateOrDeleteResourceView):

    def delete(self, request, pk):

        return HttpResponse("DELETE OK")

    def patch(self, request, pk):

        return HttpResponse("PATCH OK")

    def put(self, request, pk):

        return HttpResponse("PUT OK")


@method_decorator(ensure_csrf_cookie, name="get")
class SetCSRFTokenView(View):
    def get(self, request):

        context = RequestContext(request, {})
        django_engine = engines["django"]

        template = django_engine.from_string("{% csrf_token %}GET OK")
        rendered_template = template.template.render(context)

        return HttpResponse(rendered_template)

