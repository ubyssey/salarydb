import os
import sys
sys.path.append('/var/webapps/salarydb/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'salarydb.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
