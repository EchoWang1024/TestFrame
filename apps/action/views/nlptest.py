# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.testservice.views import public_methods as test_service
from apps.testservice.views import report_manager as report_manager
import os


class NlpTest(object):

    def __init__(self, message, case_id, test_case, test_refs,
                 test_id,  test_tools, explain, scene, count, case_path, flog, test_result):

        self.message = message
        self.case_id = case_id
        self.version = message["version"]
        self.count = count
        self.test_case = test_case
        self.test_refs = test_refs
        self.test_id = test_id
        self.test_tools = test_tools
        self.explain = explain
        self.scene = scene
        self.case_path = case_path
        self.run_time = test_service.get_date_time(1, 0)
        self.test_result_file = ""
        self.test_result_file_gbk = ""
        self.flog = flog
        self.test_result = test_result
        self.config_file = ""
        self.answer_file = ""
        self.test_nlp()

    def test_nlp(self):

        # 将输入和输出放入到文件中
        test_service.nlp_insert_valid(self.test_id, self.test_case, self.test_refs)

        os.chdir(self.case_path + "/test")
        if self.scene == "welcome":
            os.system("python get_und_result.py " + self.case_id + " " + self.test_id + "welcome")
        else:
            os.system("python get_und_result.py " + self.case_id + " " + self.test_id)

        print "用例:" + str(self.case_id) + "测试结束"
        report_manager.nlptest_result(self.test_id, self.explain, self.case_path,
                                      self.count, self.case_id, self.flog, self.test_result)
