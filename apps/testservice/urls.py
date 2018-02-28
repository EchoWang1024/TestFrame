
from django.conf.urls import url
from django.contrib import  admin
from apps.testservice.views import testlistner as service_views
from apps.testservice.views import display

urlpatterns = [

    url(r'^/$', service_views.test_listner, name='service'),

]