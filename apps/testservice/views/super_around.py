# -*- coding: utf-8 -*-
from apps.testservice import models as mysql_db
from main_test import main_test
import send_email
import super_butt
import MySQLdb
import public_methods
import os
import time


def super_around(message):
    logger, fh, ch = public_methods.set_logger()
    try:
        table_name = message["tableName"]
        case_id = message["caseId"]
        times = int(message["times"])
        mail_valid = message["mail_valid"]
        # 创建test_id
        try:
            test_id = mysql_db.TestFrame.objects.order_by('-test_id')[0].test_id
            test_id = str(int(test_id) + 1)
        except Exception as e:
            print ("创建test_id 10000001") + str(e)
            test_id = "10000001"
        # 记录本次测试参数
        if message["test_wait"] is True:
            message.setdefault('status', '4')
        else:
            message.setdefault('status', '1')
        case_type = case_id.split('_')[0]
        try:
            public_methods.inert_tastframe(
                test_id,
                case_id,
                case_type,
                message['tableName'],
                message['version'],
                message['status'],
                message["start_time"]
            )
        except Exception as e:
            print ("next") + str(e)
        # 判断状态为4的话等待300秒，否则不等待。
        valid = mysql_db.TestFrame.objects.get(test_id=test_id)
        if valid.state == "4":
            time.sleep(300)
            valid.state = "1"
            valid.save()
        # 数据表名称
        sql_table_name = table_name.split(".")[0]
        database = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="test", charset="utf8")
        cursor = database.cursor()
        sql_find = "select * from " + sql_table_name + " where id = " + "'" + case_id + "'"
        sql_result = cursor.execute(sql_find)
        sql_find_list = cursor.fetchmany(sql_result)
        sql_next_id = sql_find_list[0][5]
        # 获取next_id列表
        if sql_next_id == "[0]":
            next_id_list = [case_id]
        else:
            next_id_list = public_methods.get_next_caseid(sql_next_id)

        # 判断测试类型打开不同测试类型所需要的文件，避免在循环中重复打开大文件．

        if case_type == "nlp":
            tool_path = public_methods.get_ini("nlptool_path")
            result_path = public_methods.get_ini("result_path")
            case_path = str(result_path) + "/" + message['version'] + "-" + test_id
            os.system("mkdir " + case_path)
            os.system("cp -rf " + tool_path + " " + case_path)
            return_faillog = open(case_path + "/return_log.txt", "a+")
            test_result = open(case_path + "/result.txt", "a+")
            main_test(times, next_id_list, sql_table_name, cursor, test_id, case_type,
                      message, case_path, return_faillog, test_result)
            return_faillog.close()
            test_result.close()
        elif case_type == "pstt":
            # 创建test_result文件夹
            result_path = public_methods.get_ini("result_path")
            pstt_path = public_methods.get_ini("pstt_path")
            case_path = result_path + "/pstt-" + test_id
            os.system("mkdir " + case_path)
            # 将pstt工具拷贝到该文件夹下
            os.system("cp -rf " + pstt_path + " " + case_path)
            # 打开reslt文件
            test_result = open(case_path + "/pstt/pstt_client-4.1.0/result.txt", "a+")
            main_test(times, next_id_list, sql_table_name, cursor, test_id, case_type, message, case_path,
                      "", test_result)
        else:
            main_test(times, next_id_list, sql_table_name, cursor, test_id, case_type, message, "", "", "")

        # close cursor and database
        cursor.close()
        database.close()
        # in case_path
        super_butt.final_butt(test_id, case_type, times, message, case_path)
        # send email
        if mail_valid == "0":
            send_email.send_email_manager(message, test_id, case_path)
        else:
            print ("不发送邮件")
    except:
        logger.exception("Exception Logged")



