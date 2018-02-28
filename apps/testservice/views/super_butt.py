# coding=utf-8

from apps.testservice import models as mysql_db
import public_methods
import threading
import os


def final_butt(test_id, case_type, times, message, case_path):
    report_folder = "/part/home/pachiratest/report"
    # 将数据库状态更改为已完成, 将下载地址存入数据库
    valid = mysql_db.TestFrame.objects.get(test_id=test_id)
    if valid.state == "3":
        pass
    else:
        valid.state = '2'
        valid.save()

    if case_type == "nlp":
        table_name_cut = message["tableName"].split(".")[0]
        public_methods.insert_table(test_id, report_folder + "/" + test_id + "-" + table_name_cut, "resultPath", "")
        nlp_file_fata = open(case_path + "/result_fata.txt", "a+")
        nlp_file_fata.write("＞＞＞＞测试编号：" + test_id + "\n" +
                            "＞＞＞＞测试表格名称：" + message['tableName'] + "\n" +
                            "＞＞＞＞测试执行次数：" + str(times) + "\n" +
                            "＞＞＞＞测试结果统计如下：" + "\n")
        for count in range(1, int(times) + 1):
            try:
                nlp_count = mysql_db.NlpCount.objects.get(test_id=str(test_id), count=str(count))
                nlp_true = nlp_count.nlp_true
                nlp_fail = nlp_count.nlp_fail
                if nlp_fail == 0:
                    nlp_file_fata.write("－－＞＞"
                                        + "第" + str(count)
                                        + "轮测试成功；成功个数：" + str(nlp_true) + ",　失败个数：" + str(nlp_fail) + "\n")
                else:
                    nlp_file_fata.write("－－＞＞"
                                        + "第" + str(count)
                                        + "轮测试失败；成功个数：" + str(nlp_true) + ",　失败个数：" + str(nlp_fail) + "\n")
            except:
                pass

        nlp_file = open(case_path + "/result.txt", "r")
        nlp_file_all = nlp_file.read()
        nlp_file.close()
        nlp_file_fata.write("\n" + nlp_file_all)
        nlp_file_fata.close()
        # 转换格式为gbk ,并将文件放入到结果文件夹中
        os.system("iconv -f utf-8 -ct gbk " + case_path + "/result_fata.txt > " + case_path + "/result_gbk.txt")
        os.system("zip " + test_id + "-" + table_name_cut + ".zip " + case_path + "/result_gbk.txt")
        os.system(
            "cp " + case_path + "/result_gbk.txt " + report_folder + "/" + test_id + "-" + table_name_cut + "_gbk.txt")
        os.system("cp " + case_path + "/result_gbk.txt " + report_folder + "/" + test_id + "report_gbk.txt")
        # 将错误log也输出到结果文件夹中
        os.system("iconv -f utf-8 -ct gbk " + case_path + "/return_log.txt > " + case_path + "/return_log_gbk.txt")
        os.system(
            "cp " + case_path + "/return_log_gbk.txt " + report_folder + "/" + test_id + "-" + table_name_cut + "_flog.txt")
        os.system("cp " + case_path + "/return_log_gbk.txt " + report_folder + "/" + test_id + "report_flog.txt")
        print ("repeot over!")
    elif case_type == "pstt":
        table_name_cut = message["tableName"].split(".")[0]
        public_methods.insert_table(test_id, report_folder + "/" + test_id + "-" + table_name_cut, "resultPath", "")
        os.system("iconv -f utf-8 -ct gbk " + case_path + "/pstt/pstt_client-4.1.0/result.txt > "
                  + case_path + "/result_gbk.txt")
        os.system("zip " + case_path + "/" + test_id + "-" + table_name_cut + ".zip " + case_path + "/result_gbk.txt")
        os.system(
            "cp " + case_path + "/result_gbk.txt " + report_folder + "/" + test_id + "-" + table_name_cut + "_gbk.txt")
        os.system("cp " + case_path + "/result_gbk.txt " + report_folder + "/" + test_id + "report_gbk.txt")
    else:
        public_methods.insert_table(test_id, report_folder + "/" + test_id + "report", "resultPath", "")
    print threading.current_thread().getName() + " test overs -----------"
