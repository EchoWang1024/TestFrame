# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.testservice.views import public_methods as test_service
# from apps.testservice.views import check_test as check_test
from apps.testservice.views import report_manager as report_manager
from apps.testservice import models as mysql_db
import time
import os
import codecs
import threading


class NluTest(object):

    def __init__(self, message, test_case, test_id, data, test_tools, explain, port, test_refs):

        self.message = message
        self.case_id = message["caseId"]
        self.url = message["url"]
        self.version = message["version"]

        try:
            self.count = self.message["count"]
        except KeyError:
            self.count = 1

        self.test_case = eval(test_case)
        self.data = data
        self.test_id = test_id
        self.test_tools = test_tools
        self.explain = explain
        self.port = port
        self.input_file = self.test_case["inputFile"]
        self.standard_file = self.test_case["standardFile"]
        self.report_folder = "/part/home/pachiratest/report"
        self.run_time = test_service.get_date_time(1, 0)
        self.test_result_file = ""
        self.test_result_file_gbk = ""

        self.config_file = ""
        self.answer_file = ""

        if self.input_file != "" or self.standard_file != "":

            self.decoder_config = self.data["path"]
            self.test_nludecoder()

        report_manager.nlutest_result(self.test_result_file_gbk, self.test_id,
                                      self.message, self.report_folder, self.explain)
        print 'test ok!!!'

    def test_nludecoder(self):
        # 获取当前路径
        pwd = os.getcwd()
        print pwd
        test_folder = self.version + "-" + self.test_id
        test_path = self.data["path"]
        os.chdir(test_path)
        os.system('mkdir' + ' ' + test_folder)
        case_path = test_path + '/' + test_folder

        # 拷贝工具到文件夹内
        os.chdir(case_path)
        os.system('cp -rf /part/home/pachiratest/t/lj/test/*' + ' ' + case_path)
        os.system("cp /part/home/pachiratest/t/lj/nluOffline_test/projects/*.txt" + " "
                  + case_path)
        os.system("cp /part/home/pachiratest/t/lj/nluOffline_test/projects/*.xml" + " "
                  + case_path)
        os.system('chmod +x '+self.test_tools)

        input_cut = self.input_file.split("/")[-1]
        standard_cut = self.standard_file.split("/")[-1]
        input_path = case_path + "/" + input_cut
        standard_path = case_path + "/" + standard_cut
        port = int(float(self.port))
        print "===============================" + os.getcwd()
        os.system('./' + str(self.test_tools) + ' ' + str(input_path) + ' ' + str(standard_path)
                  + " " + str(port))
        print('./' + str(self.test_tools) + ' ' + str(input_path) + ' ' + str(standard_path)
              + " " + str(port))
        # 将out文件放如到该文件夹下
        report_folder = "/part/home/pachiratest/report/"
        os.system("mv out.xml " + report_folder + self.test_id + "report_out.xml")
        self.test_result_file_gbk = str(case_path) + "/result"
        print self.test_result_file_gbk
        os.chdir(pwd)
        print 'ok'



