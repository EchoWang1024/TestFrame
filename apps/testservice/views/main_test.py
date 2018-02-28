# -*- coding: utf-8 -*-
from apps.action.views import asrtest as asrtest
from apps.action.views import nlutest as nlutest
from apps.action.views import nlptest as nlptest
from apps.testservice import models as mysql_db
from apps.action.views import PsttTest
from django.shortcuts import redirect
import public_methods
import os
import time
shun_test_id = ""


def main_test(times, next_id_list, sql_table_name, cursor, test_id, case_type, message, case_path, flog, test_result):
    # 外层循环－－－－－－－－－－－count
    for count in range(1, int(times) + 1):
        count = str(count)
        if case_type == "nlp":
            flog.write("------------------------------------------------"
                       + '第' + str(count) + '轮测试'
                       + "------------------------------------------------\n")
            test_result.write("-----------------------------------------------------------------"
                              + test_id + " " + '第' + str(count) + '轮测试'
                              + "------------------------------------------------------------"
                              + "\n"
                              )
        elif case_type == "pstt":
            test_result.write("----------------------------------------------------------\n"
                              + "|" + (test_id + " " + '第' + str(count) + '轮测试').center(62) +"|\n"
                              + "----------------------------------------------------------\n\n"
                              )
        # 内层内层－－－－－－－－－－case_id
        for case_id in next_id_list:
            if shun_test_id == test_id:
                print test_id + " has been kill !!!"
                break
            # 数据表查询
            sql_run = "select * from " + sql_table_name + " where id = " + "'" + case_id + "'"
            sql_run_result = cursor.execute(sql_run)
            sql_run_result_list = cursor.fetchmany(sql_run_result)
            # 通过case_id从数据表中获取对应进行取值
            scene = sql_run_result_list[0][1]
            test_case = sql_run_result_list[0][2].strip()
            data = eval(sql_run_result_list[0][3].strip())
            test_tools = sql_run_result_list[0][4]
            test_refs = sql_run_result_list[0][6].strip()
            explain = sql_run_result_list[0][7]
            try:
                port = sql_run_result_list[0][8]
            except Exception as e:
                print "在表格中查询port－－" + str(e)
                pass

            # 在执行工具前，将当前执行的用例存入数据库
            public_methods.insert_test_frame_speed(count, case_id, test_id)

            # 判断测试类型，执行相应的测试方法
            if case_type == "asr":
                asrtest.AsrTest(message, test_case, test_id, data, test_tools, explain, test_refs)
            elif case_type == "nlu":
                nlutest.NluTest(message, test_case, test_id, data, test_tools, explain, port, test_refs)
            elif case_type == "nlp":
                nlptest.NlpTest(message, case_id, test_case, test_refs,
                                test_id, test_tools, explain, scene, count, case_path, flog, test_result)
            elif case_type == "pstt":
                # # 端口验证
                project_path = os.path.dirname(__file__)
                pstt_port_file = os.path.join(project_path, "../../../pstt-port.txt")
                while True:
                    with open(pstt_port_file, "r") as f:
                        f_read = f.read()
                    if f_read.strip() == "":
                        valid = mysql_db.TestFrame.objects.get(test_id=test_id)
                        valid.state = "4"
                        valid.save()
                        time.sleep(20)
                    else:
                        valid = mysql_db.TestFrame.objects.get(test_id=test_id)
                        valid.state = "1"
                        valid.save()
                        break
                # 测试
                PsttTest.PsttTest(message, test_case, test_id, data, test_tools, explain, test_refs, scene, case_path,
                                  count, case_id, test_result)
            else:
                print ("暂不支持的测试类型")


def shut_down(request):
    global shun_test_id
    shun_test_id = request.GET.get("test_id")
    valid = mysql_db.TestFrame.objects.get(test_id=shun_test_id)
    valid.state = '3'
    valid.save()
    return redirect("/test_task1")
