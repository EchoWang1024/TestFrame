# -*- coding: utf-8 -*-
"""TestFrame URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
from apps.testservice.views import execution_test
from apps.testservice.views import send_email
from apps.testservice.views import upload_file
from apps.testservice.views import test_task
from apps.testservice.views import test_case
from apps.testservice.views import testlistner as service_views
from apps.testservice.views import main_test

urlpatterns = [
    # 首页
    url(r'^$', execution_test.home),
    url(r'^testframe_log/$', execution_test.home_handle),
    # 视图execution_test下
    url(r'^test_start/$', service_views.test_listner, name="service"),
    url(r'^test/$', execution_test.execution_test),
    url(r'^new_test/$', execution_test.execution_test_5),
    url(r'^caseid_valid/$', execution_test.caseid_valid),
    url(r'^table_valid/$', execution_test.table_valid),
    url(r'^sheet_valid/$', execution_test.sheet_valid),
    # 视图test_task下
    url(r'^test_task_handle(\d+)/$', test_task.test_task_handle),
    url(r'^test_task(\d+)/$', test_task.test_task),
    url(r'^(\d+)/$', test_task.test_task_download),
    url(r'^nlu(\d+)/$', test_task.test_task_nludownload),
    url(r'^nlpflog(\d+)/$', test_task.nlp_flog_download),
    # 视图test_case下
    url(r'^test_case(\d+)/$', test_case.test_case),
    url(r'^test_case_handle(\d+)/$', test_case.test_case_handle),
    url(r'^case/(.+)/$', test_case.test_case_download),
    url(r'^del/(.+)/$', test_case.test_case_del),
    url(r'^test_case_del/$', test_case.test_case_del_most),
    # 发送邮件
    url(r'^send_email/$', send_email.send_email),
    # 文件上传
    url(r'^up_load/$', upload_file.up_load),
    url(r"^upload_bar/$", upload_file.show_progress),
    url(r'^admin/', admin.site.urls),
    url(r'^uploadmail/$', upload_file.upload_mailaddress),
    url(r'^mail_task/$', upload_file.mail_task),
    url(r'^mail_task_handle/$', upload_file.mail_task_handle),
    url(r'^mail_del/(.+)', upload_file.upload_mailaddress_del),
    # 强制杀死
    url(r"^thread_kill/$", main_test.shut_down)
]
