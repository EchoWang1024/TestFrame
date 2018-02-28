# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CheckTest(models.Model):

    test_id = models.CharField(max_length=32, unique=True)
    case_id = models.CharField(max_length=32, null=True)
    next_id = models.TextField(null=True)
    left_next_id = models.TextField(null=True)
    count = models.CharField(max_length=32, null=True)
    times = models.CharField(max_length=32, null=True)
    now_case_id = models.CharField(max_length=32, null=True)
    now_sheet = models.CharField(max_length=64, null=True)
    left_sheet = models.CharField(max_length=1024, null=True)
    '''
    test_id:执行id
    caseId:启动测试的用例id
    nextid:本次除caseId外所需要执行的caseId
    count:当前执行到第几次
    times:总计要执行多少次
    nowCaseId:当前执行的caseId
    leftNextId:剩余要执行的caseId
    '''

    def __unicode__(self):
        return self.test_id, self.case_id, self.next_id, self.count, self.times, self.now_case_id, self.left_next_id


class TestPath(models.Model):

    table_name = models.CharField(max_length=1024, null=True)
    table_path = models.CharField(max_length=512, editable=False, blank=True)


class ResultPath(models.Model):

    test_id = models.CharField(max_length=512, null=False)
    tools_log_path = models.CharField(max_length=512, null=True)
    result_path = models.CharField(max_length=512, null=True)


class TestFrame(models.Model):

    test_id = models.CharField(max_length=32, unique=True)
    case_id = models.CharField(max_length=32, null=True)
    entry_name = models.CharField(max_length=32, null=True)
    table_name = models.CharField(max_length=1024, null=True)
    version_num = models.CharField(max_length=32, null=True)
    state = models.CharField(max_length=32, null=True)
    start_time = models.CharField(max_length=128, null=True)
    speed = models.CharField(max_length=32, null=False, default="0%")


class Mail(models.Model):

    username = models.CharField(max_length=32, null=True)
    mailaddress = models.CharField(max_length=64, null=True)
    asr_state = models.CharField(max_length=32, null=True)
    nlu_state = models.CharField(max_length=32, null=True)
    nlp_state = models.CharField(max_length=32, null=True)


class NlpCount(models.Model):
    test_id = models.CharField(max_length=32, unique=True)
    count = models.CharField(max_length=32, null=True)
    nlp_true = models.IntegerField(default=0)
    nlp_fail = models.IntegerField(default=0)

    '''结束'''