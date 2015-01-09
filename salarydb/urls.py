from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^salaries/', include('main.urls')),
)
