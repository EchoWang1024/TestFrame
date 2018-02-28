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


class AsrTest(object):

    def __init__(self, message, test_case, test_id, data, test_tools, explain, test_refs):
        self.message = message
        self.case_id = message["caseId"]
        self.url = message["url"]
        self.version = message["version"]

        try:
            self.count = self.message["count"]
        except KeyError:
            self.count = 1

        self.test_case = test_case
        self.data = data
        self.test_id = test_id
        self.test_tools = test_tools
        self.explain = explain

        self.case_list = self.test_case["voicelist"]
        self.answer_list = self.test_case["answer"]

        self.run_time = test_service.get_date_time(1, 0)
        self.test_result_file = ""
        self.report_folder = "/part/home/pachiratest/report"
        self.test_result_file_gbk = ""

        self.config_file = ""
        self.answer_file = ""

        if self.case_list != "" or self.answer_list != "":

            self.decoder_config = self.data["config"]
            self.test_hawkdecoder()

        else:

            self.tool_path = self.data["path"]
            self.test_gtest()

        report_manager.hawkdecoder_result(self.test_result_file_gbk, self.test_id, self.message,
                                          test_refs, self.report_folder, self.count, self.explain)
        # check_test.check_test(self.message, self.test_id, "asrtest")

    def test_hawkdecoder(self):

        pwd = os.getcwd()
        test_folder = self.version+"-" + self.case_id+"-" + self.test_id

        test_path_dict = self.data["config"].split("/")
        self.config_file = test_path_dict[len(test_path_dict)-1]
        test_path = test_service.get_path(test_path_dict)

        answer_path_dict = self.test_case["answer"].split("/")
        answer_path = test_service.get_path(answer_path_dict)

        result_path, log_path = test_service.mkdir(test_path, test_folder)

        case_path = test_path + test_folder
        os.chdir(pwd)

        # 执行存入数据库方法

        if self.url != "":

            url_list = self.url.values()

            for i in range(len(url_list)):

                url = url_list[i]
                test_service.download(url, case_path + "/")

        os.chdir(case_path)

        os.system('chmod +x '+self.test_tools)
        asr_log = str(result_path) + "/" + str(self.count) + ".log"
        asr_result = str(result_path) + "/" + str(self.count)

        print self.case_id, "do test----", self.test_id, "-----", threading.current_thread().getName()

        os.system("./" + str(self.test_tools) +
                  " --config " + str(self.decoder_config) +
                  " --filelist " + str(self.case_list) +
                  " --log " + str(asr_result) +
                  " --sleep 2 >>" + asr_log
                  )

        print "./" + str(self.test_tools) + " --config " + str(self.decoder_config) + " --filelist "\
              + str(self.case_list) + " --log " + str(asr_result) + " --sleep 2 >>"+asr_log

        os.chdir(answer_path)

        os.system("python pasr_calc_recrate.py -s sclite -m " +
                  str(self.answer_list) +
                  " -r "+str(asr_result) +
                  " -o "+str(asr_result) +
                  "rate"
                  )

        print "python pasr_calc_recrate.py -s sclite -m " + str(self.answer_list) + " -r "\
              + str(asr_result) + " -o " + str(asr_result) + "rate"

        test_result = open(str(asr_result)+"rate")

        lines = []
        erase = False
        for line in test_result:
            if line.strip() == "Real time(s):".encode("utf-8"):
                erase = True
            if not erase:
                lines.append(line)
            if line.strip() == "W-------------------------------------------------------".encode("utf-8"):
                erase = False
            if line.strip() == "========================================================".encode("utf-8"):
                erase = True

        test_result.close()

        self.test_result_file = str(asr_result)+"rate_result.txt"
        open(self.test_result_file, 'w').writelines(lines)

        asr_rt = codecs.open(asr_log, 'r', 'utf-8')
        rt = ",rt:"

        global wrt

        for line in reversed(asr_rt.readlines()):
            if rt in line:
                r_line = line.split(rt)[1]
                wrt = "R T : "+r_line
                asr_rt.close()

        test_result_rt = codecs.open(str(self.test_result_file), 'r+', 'utf-8')
        read_test_result = test_result_rt.read()
        test_result_rt.seek(0)

        try:
            test_result_rt.write('\n')
            test_result_rt.write(wrt+'\n')
            test_result_rt.write(read_test_result)
            test_result_rt.close()
        except Exception as e:
            print e
            print "testError"

        self.test_result_file_gbk = str(asr_result)+"rate_result_gbk.txt"

        os.system("iconv -f utf-8 -t gbk "+self.test_result_file+" >"+self.test_result_file_gbk)

        print pwd

        os.chdir(pwd)
        time.sleep(1)

    def test_gtest(self):

        pwd = os.getcwd()
        test_folder = self.version+"-" + self.case_id+"-" + self.test_id
        test_path = self.data["path"]

        case_path = test_path + test_folder

        test_service.mkdir(test_path, test_folder)

        if self.url != "":

            url_list = self.url.values()

            for i in range(len(url_list)):

                url = url_list[i]
                test_service.download(url, case_path + "/")

        os.chdir(case_path)
        os.system('chmod +x '+self.test_tools)

        case_path = mysql_db.TestPath.objects.values('table_path')[0]['table_path']
        os.chdir(case_path)
        os.system('./startgtest.sh ' + test_folder + " & >>test.log")

        # os.system("./" + str(self.test_tools) + " --gtest_output=xml:1.xml " + str(self.tool_path))
        os.chdir(pwd)
        time.sleep(2)
