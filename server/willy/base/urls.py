__author__ = 'hieutran'

from django.conf import settings
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static

urlpatterns = patterns(
    '',
    url(r'^api/blog/account/', include("blog.account.account_urls")),
    url(r'^api/blog/test', include("blog.test.test_urls")),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)