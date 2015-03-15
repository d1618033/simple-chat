from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'samplechatsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^simplechat/', include('simplechat.urls', namespace='simplechat')),
    url(r'^simplechat/api/', include('simplechat_api.urls', namespace='simplechat_api')),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

