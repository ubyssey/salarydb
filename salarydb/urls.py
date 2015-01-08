from django.conf.urls import patterns, include, url

from main import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.landing', name='landing'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/search/?$', views.api_search),
    url(r'^api/vote/(\d*)/?$', views.api_vote),
    url(r'^api/faculty/(\d*)/?$', views.api_faculty),
    #url(r'^employee/([a-zA-Z-]*)/?$', views.employee),
    url(r'^employee/(?P<first>[a-zA-Z]*)-(?P<last>[a-zA-Z-]*)/?$', views.employee),
    url(r'^search/?$', views.search),
    url(r'^search/(\d*)/?$', views.search),
    url(r'^admin/', include(admin.site.urls)),
)
