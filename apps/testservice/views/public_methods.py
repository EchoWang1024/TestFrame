# coding=utf-8

from apps.testservice import models as mysql_db
import datetime
import urllib
import time
import logging
import ConfigParser
from socket import *
from django import db
import os


def get_next_caseid(next_id):

    if next_id != 0:

        next_id_list = []

        if "-" in next_id:

            start_id = next_id.split("-")[0].split("_")
            end_id = next_id.split("-")[1].split("_")

            for i in range(int(start_id[1]), int(end_id[1])+1):
                next_id_list.append(start_id[0]+"_"+str(i))

        elif "[" in next_id:
            if next_id.replace('[', ''):
                next_id = next_id.replace('[', '')
                next_id = next_id.replace(']', '')
            next_id = next_id.replace('u', '')
            next_id = next_id.replace('', '')
            next_id = next_id.replace(' ', '')
            next_id = next_id.replace('\'', '')
            next_id_list = next_id.split(',')
        else:
            next_id_list = next_id.split(",")

        return next_id_list

    else:
        return next_id


def download(url, path):

    download_file = url.split("/")[len(url.split("/"))-1]
    path = path + download_file

    def reporthook(a, b, c):
        per = 100.0 * a * b / c

        if per > 100:
            per = 100
            print '%.2f%%' % per
        elif per == 100:
            print '%.2f%%' % per

    urllib.urlretrieve(url, path, reporthook)


def get_date_time(file_name, now_time):

    date_time = datetime.datetime.now()

    if file_name == 1 and now_time == 0:

        input_year = date_time.year
        input_month = date_time.month
        input_day = date_time.day
        input_hour = date_time.hour
        input_minute = date_time.minute
        input_second = date_time.second
        microsecond_time = date_time.microsecond

        imput_datetime = datetime.datetime(
                year=int(input_year),
                month=int(input_month),
                day=int(input_day),
                hour=int(input_hour),
                minute=int(input_minute),
                second=int(input_second)
        )
        format_time = long(round(time.mktime(imput_datetime.timetuple())))

        now_time = long(str(format_time) + str(microsecond_time/1000))

        return now_time

    else:
        return date_time


def mkdir(test_path, test_folder):

    os.chdir(test_path)
    try:
        os.makedirs(test_folder)
        os.chdir(test_folder)
        os.makedirs("result")
        os.makedirs("log")

    except Exception as e:
        print e

    result = str(test_path) + str(test_folder) + "/" + "result"
    log = str(test_path) + str(test_folder) + "/" + "log"
    return result, log


def mkdir2(test_path, test_folder):

    os.chdir(test_path)
    try:
        os.makedirs(test_folder)
        os.chdir(test_folder)
        os.makedirs("result")
        os.makedirs("log")

    except Exception as e:
        print e

    result = str(test_path) + '/' +str(test_folder) + "/" + "result"
    log = str(test_path) + '/' +str(test_folder) + "/" + "log"
    return result, log


def get_path(path_dict):

    path = ""

    for i in range(1, len(path_dict)-1):
        path = path + "/" + path_dict[i]

    return path + "/"


def get_path2(path_dict):

    path = ""

    for i in range(len(path_dict)-1):
        path = path + "/" + path_dict[i]

    return path + "/"


def insert_table(test_id, file_path, type_name, args):

    if type_name == "resultPath":

        result = mysql_db.ResultPath()
        result.test_id = test_id
        result.result_path = file_path
        result.save()
        db.reset_queries()
    elif type_name == "testPath":

        table_name = args
        result = mysql_db.TestPath()
        result.table_name = table_name
        result.table_path = file_path
        result.save()
        db.reset_queries()


def inert_tastframe(test_id, case_id, entry_name, table_name, version_num, status, start_time):

    result = mysql_db.TestFrame()
    result.test_id = test_id
    result.case_id = case_id
    result.entry_name = entry_name
    result.table_name = table_name
    result.version_num = version_num
    result.state = status
    result.start_time = start_time
    result.save()
    db.reset_queries()


# 进行tomcat重启
def nlpurl_valid(url_dict):
    print url_dict
    tcpClientSocket = socket(AF_INET, SOCK_STREAM)
    serAddr = ('192.168.128.57', 7788)
    tcpClientSocket.connect(serAddr)
    tcpClientSocket.send(str(url_dict))
    # 接收对方发送过来的数据，最大接收1024个字节
    print("等待返回数据...")
    recvData = tcpClientSocket.recv(1024)
    print recvData
    print "数据服务器重启完成."
    # 关闭套接字
    tcpClientSocket.close()


# 插入speed字段到testframe
def insert_test_frame_speed(count, case_id, test_id):
    speed = "第" + str(count) + "轮：" + str(case_id)
    mysql_db.TestFrame.objects.filter(test_id=test_id).update(speed=speed)


'''2.0版本开发'''


# 将表格值插入到文件中
def nlp_insert_valid(test_id, table_test, table_refs):
    table_path = "/part/home/pachiratest/nlptest/" + test_id
    if os.path.exists(table_path):
        pass
    else:
        os.system("mkdir " + table_path)

    pwd = os.getcwd()
    os.chdir(table_path)
    file_test = open("test.txt", "w")
    print table_test
    file_test.write(str(table_test))
    file_test.close()
    file_refs = open("refs.txt", "w")
    file_refs.write(str(table_refs))
    file_refs.close()
    os.chdir(pwd)


# 将message信息写入到文件中去
def nlp_message(thread_name, message):
    table_path = "/part/home/pachiratest/nlptest/" + thread_name
    if os.path.exists(table_path):
        pass
    else:
        os.system("mkdir " + table_path)

    pwd = os.getcwd()
    os.chdir(table_path)
    file_message = open("message.txt", "w")
    file_message.write(str(message))
    file_message.close()
    os.chdir(pwd)


def set_logger():

    # 创建一个logger,可以考虑如何将它封装
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)

    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler(os.path.join("/part/home/pachiratest/mylog", 'TestFrame_log.txt'))
    fh.setLevel(logging.DEBUG)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s.%(lineno)d - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 清空logger.handlers
    logger.handlers = []
    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger, fh, ch


'''2.1版本开发'''


# 读取配置文件
def get_ini(ini_type):
    project_path = os.path.dirname(__file__)
    ini_file = os.path.join(project_path, "../../../testservice.ini")
    f = open(ini_file)
    config = ConfigParser.ConfigParser()
    config.readfp(f)
    result = config.get("MAIN_TEST", ini_type)
    f.close()
    return result










