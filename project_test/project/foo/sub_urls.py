"""
Foo sub included urls
"""
from django.conf.urls import url

from django.views.generic.base import TemplateView

urlpatterns = [
    # Foo section
    url(r'^$', TemplateView.as_view(
        template_name="page.html"
    ), name='index'),
    url(r'^plop/$', TemplateView.as_view(
        template_name="page.html"
    ), name='plop'),
]
