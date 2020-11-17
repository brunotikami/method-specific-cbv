from django.urls import path
from django.conf.urls import url
from django.views.generic import RedirectView

from tests.v1.dummy_project.dummy_app.views import DummyCreateResourceView
from tests.v1.dummy_project.dummy_app.views import DummyUpdateOrDeleteResourceView
from tests.v1.dummy_project.dummy_app.views import SetCSRFTokenView

urlpatterns = [
    path('create/<int:pk>/', DummyCreateResourceView.as_view(), name='create'),
    path('update_or_delete/<int:pk>/', DummyUpdateOrDeleteResourceView.as_view(), name='update_or_delete'),
    path('give_me_a_csrf_token/', SetCSRFTokenView.as_view(), name='set_csrf_token'),
]

