from django.conf.urls import patterns, include, url
from django.contrib import admin

import salarydb.views as views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^salaries/?$', views.landing, name='landing'),
    url(r'^salaries/api/search/?$', views.api_search),
    url(r'^salaries/api/vote/(\d*)/?$', views.api_vote),
    url(r'^salaries/api/faculty/(\d*)/?$', views.api_faculty),
    url(r'^salaries/employee/(?P<first>[a-zA-Z]*)-(?P<last>[a-zA-Z-\']*)/?$', views.employee),
    #url(r'^employee/(?P<slug>[a-zA-Z-\']*)/?$', views.employee),
    url(r'^salaries/search/?$', views.search),
    url(r'^salaries/search/(\d*)/?$', views.search),
    url(r'^salaries/admin/', include(admin.site.urls)),
)
