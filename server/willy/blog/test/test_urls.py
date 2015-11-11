__author__ = 'hieutran'

from django.conf.urls import patterns, url
from blog.test import test_views

urlpatterns = patterns(
    '',
    url(r'^$', test_views.TestView.as_view()),
)
