from django.conf.urls import patterns, include, url
import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.landing, name='landing'),
    url(r'^api/search/?$', views.api_search),
    url(r'^api/vote/(\d*)/?$', views.api_vote),
    url(r'^api/faculty/(\d*)/?$', views.api_faculty),
    url(r'^employee/(?P<first>[a-zA-Z]*)-(?P<last>[a-zA-Z-\']*)/?$', views.employee),
    #url(r'^employee/(?P<slug>[a-zA-Z-\']*)/?$', views.employee),
    url(r'^search/?$', views.search),
    url(r'^search/(\d*)/?$', views.search),
    url(r'^admin/', include(admin.site.urls)),
)
