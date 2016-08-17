from django.conf.urls import patterns, include, url
from django.contrib import admin

import salarydb.views as views

admin.autodiscover()

salarydb_patterns = [
    url(r'^$', views.landing, name='landing'),
    url(r'^api/search/?$', views.api_search),
    url(r'^api/vote/(\d*)/?$', views.api_vote),
    url(r'^api/faculty/(\d*)/?$', views.api_faculty),
    url(r'^employee/(?P<first>[a-zA-Z]*)-(?P<last>[a-zA-Z-\']*)/?$', views.employee),
    #url(r'^employee/(?P<slug>[a-zA-Z-\']*)/?$', views.employee),
    url(r'^search/?$', views.search),
    url(r'^search/(\d*)/?$', views.search),
    url(r'^admin/', include(admin.site.urls))
]

urlpatterns = [
    url(r'^', include(salarydb_patterns)),
    url(r'^salaries/', include(salarydb_patterns))
]
