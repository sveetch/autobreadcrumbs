"""
Foo urls should contains every cases
"""
from django.conf.urls import include, url

from django.views.generic.base import TemplateView

urlpatterns = [
    # Foo section
    url(r'^$', TemplateView.as_view(
        template_name="page.html"
    ), name='index'),
    url(r'^pika/$', TemplateView.as_view(
        template_name="page.html"
    ), name='pika'),
    url(r'^pika/chu/$', TemplateView.as_view(
        template_name="page.html"
    ), name='pika-chu'),

    # Url with some numeric args (year + month)
    url(r'^date/(?P<year>\d{4})/(?P<month>\d{2})/$', TemplateView.as_view(
        template_name="page.html"
    ), name='year-month'),

    # Url with a string arg
    url(r'^sluggy/(?P<slug>[-\w]+)/$', TemplateView.as_view(
        template_name="page.html"
    ), name='slug'),

    # Sub included section with its own namespace
    url(r'^sub/', include('project.foo.sub_urls', namespace='subfoo')),

    # Invisible sub section has no crumb but its children have one
    url(r'^invisible/$', TemplateView.as_view(
        template_name="page.html"
    ), name='invisible'),

    url(r'^invisible/chu/$', TemplateView.as_view(
        template_name="page.html"
    ), name='invisible-chu'),
]
