__author__ = 'hieutran'

from django.conf.urls import patterns, url

from blog.account import account_views

urlpatterns = patterns(
    '',
    url(r'^register', account_views.AccountRegView.as_view()),
    url(r'^verify', account_views.AccountVerifyView.as_view()),
)