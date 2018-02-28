# coding=utf-8
# 邮件发送编码错误解决
from django.core.mail import send_mail, EmailMultiAlternatives
from apps.testservice import models as mysql_db
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def send_email_manager(message, test_id, case_path):
    table_name_cut = message["tableName"].split(".")[0]
    report_file_gbk = test_id + "-" + table_name_cut + ".zip"
    case_type = message["caseId"].split("_")[0]
    if case_type == "asr":
        # 读取数据库邮箱列表
        mailaddress = []
        mail = mysql_db.Mail.objects.all()
        for i in mail:
            if i.asr_state == '1':
                mailaddress.append(i.mailaddress)
        if len(mailaddress) != 0:
            filepath = report_file_gbk
            send_email(mailaddress, filepath, "asr测试报告", "asr测试报告详情请见附件")
            print('asr邮件发送成功')
        else:
            print("asr邮箱列表为空")
    if case_type == "nlu":
        # 读取数据库邮箱列表
        mailaddress = []
        mail = mysql_db.Mail.objects.all()
        for i in mail:
            if i.nlu_state == '1':
                mailaddress.append(i.mailaddress)
        if len(mailaddress) != 0:
            filepath = "/part/home/pachiratest/report/" + report_file_gbk
            send_email(mailaddress, filepath, "nlu测试报告", "详情请见附件")
            print('nlu邮件发送成功')
        else:
            print("nlu邮箱列表为空")
    if case_type == "nlp":
        # 读取数据库邮箱列表
        pwd = os.getcwd()
        mailvalid = ""
        nlp_file_fata = open(case_path + "/result_fata.txt", "r")
        for line in nlp_file_fata.readlines():
            if "－" in line:
                mailvalid += line

        email_text = "您好: \n" + "    　　　您于" + str(message["start_time"]) \
                     + "时间开始的编号为" + str(test_id) + "的测试已完成.\n" \
                     + " 其中：\n " \
                     + mailvalid \
                     + "\n点击如下链接(或于附件中)查看测试报告\n" \
                     + "http://192.168.128.54/report/" + test_id + "report_gbk.txt"
        email_title = "[nlp-" + str(test_id) + "-" + str(message['tableName'] + "]测试已完成")
        email_address = []
        mail = mysql_db.Mail.objects.all()
        print os.getcwd()
        for i in mail:
            if i.nlp_state == '1':
                email_address.append(i.mailaddress)
        if len(email_address) != 0:
            filepath = report_file_gbk
            send_email(email_address, filepath, email_title, email_text)
            print('nlp邮件发送成功')
        else:
            print("nlp邮箱列表为空")


def send_email(mail_address, file_path, email_title, email_text):
    msg = EmailMultiAlternatives(email_title,
                                 email_text,
                                 'testframe@pachiratech.com', mail_address)
    # 添加附件
    msg.attach_file(file_path)
    # 发送邮件
    msg.send()
