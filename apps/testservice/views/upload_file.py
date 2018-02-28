# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.testservice import models as mysql_db
from apps.testservice.views.public_methods import insert_table
from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
import os
import MySQLdb
import xlrd
# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = BASE_DIR.split('apps')[0] + "testcase"
num_process = 0


def up_load(request):
    if request.method == 'POST':
        my_file = request.FILES.get("file", None)
        if not my_file:
            context = {'prompt': '文件为空,请选择文件后上传'}
            return render(request, 'Up_load.html', context)
        else:
            filename = mysql_db.TestPath.objects.filter(table_name=my_file.name)
            if filename:
                context = {'valid': '1'}
                return render(request, 'Up_load.html', context)
            else:
                (shortname, extension) = os.path.splitext(my_file.name)
                if (extension == '.xls' or extension == '.xlsx'):
                    destination = open(os.path.join(BASE_DIR.split('apps')[0] + "testcase", my_file.name), 'wb+')
                    # 首先统计chunk的最大值
                    chunk_sum = 0
                    for chunk in my_file.chunks():
                        chunk_sum += int(len(str(chunk)))
                    # 打开特定的文件进行二进制的写操作
                    for chunk in my_file.chunks():
                        # 分块写入文件
                        global num_process
                        num_process = 100*int(len(str(chunk))) / chunk_sum
                        destination.write(chunk)
                    destination.close()
                    # 写入数据库
                    insert_table('1', FILE_PATH, "testPath", my_file.name)
                    # 生成html文件
                    os.chdir(FILE_PATH)
                    os.system('libreoffice --invisible --convert-to html ' + my_file.name)
                    filename_cut = my_file.name.split('.')[0]
                    filename_html = filename_cut + '.html'
                    # 重命名文件
                    os.system('mv ' + filename_html + ' ' + filename_cut+'.xlsx'+'.html')
                    # 移动该文件到指定目录下
                    os.system('mv ' + filename_cut+'.xlsx'+'.html' + ' /part/home/pachiratest/htmlcase')
                    context = {'prompt': '文件上传成功'}
                    # 将该张表插入数据库－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－!>
                    book = xlrd.open_workbook(my_file.name)
                    sheet = book.sheets()[0]
                    database = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="test", charset="utf8")
                    cursor = database.cursor()
                    # 创建sql语句
                    case_id_1 = sheet.cell(1, 0).value
                    if "nlu" in case_id_1:
                        if sheet.ncols != 9:
                            context = {'prompt': 'nlu文件格式不符合要求，请检查后重新上传'}
                            valid = mysql_db.TestPath.objects.filter(table_name=my_file.name)
                            path = valid[0].table_path + '/'
                            path_name = path + my_file.name
                            if valid:
                                os.remove(path_name)
                                valid.delete()
                            return render(request, 'Up_load.html', context)
                        sql_make_table = " create table " + str(my_file.name.split(".")[0]) + \
                                         "( id text, name text, test_case text, data text," \
                                         " tools text, nextid text, expected text, test_explain text, port text);"
                        try:
                            cursor.execute(sql_make_table)
                        except:
                            pass
                        for r in range(1, sheet.nrows):
                            case_id = sheet.cell(r, 0).value
                            name = sheet.cell(r, 1).value
                            case = sheet.cell(r, 2).value
                            data = sheet.cell(r, 3).value
                            tools = sheet.cell(r, 4).value
                            nextid = sheet.cell(r, 5).value
                            expected = sheet.cell(r, 6).value
                            explain = sheet.cell(r, 7).value
                            port = sheet.cell(r, 8).value
                            # 执行sql语句
                            sql_insert_table = "insert into " + my_file.name.split(".")[0] \
                                               + " (id,name,test_case,data,tools,nextid,expected,test_explain,port) values " \
                                               + "('" + str(case_id) + "', '" \
                                               + str(name) + "', '" \
                                               + str(case) + "', '" \
                                               + str(data) + "', '" \
                                               + str(tools) + "', '" \
                                               + str(nextid) + "', '" \
                                               + str(expected) + "', '" \
                                               + str(explain) + "', '" \
                                               + str(port) + "');"
                            cursor.execute(sql_insert_table)
                            database.commit()
                    else:
                        if sheet.ncols != 8:
                            context = {'prompt': '文件格式不符合要求，请检查后重新上传'}
                            valid = mysql_db.TestPath.objects.filter(table_name=my_file.name)
                            path = valid[0].table_path + '/'
                            path_name = path + my_file.name
                            if valid:
                                os.remove(path_name)
                                valid.delete()
                            return render(request, 'Up_load.html', context)
                        sql_make_table = " create table " + str(my_file.name.split(".")[0]) \
                                         + "( id text, name text, test_case text, data text," \
                                           " tools text, nextid text, expected text, test_explain text);"
                        try:
                            cursor.execute(sql_make_table)
                        except Exception as e:
                            print e
                            pass
                        for r in range(1, sheet.nrows):
                            case_id = sheet.cell(r, 0).value
                            name = sheet.cell(r, 1).value
                            case = sheet.cell(r, 2).value
                            data = sheet.cell(r, 3).value
                            tools = sheet.cell(r, 4).value
                            nextid = sheet.cell(r, 5).value
                            expected = sheet.cell(r, 6).value
                            explain = sheet.cell(r, 7).value

                            # 执行sql语句
                            sql_insert_table = "insert into " + my_file.name.split(".")[0] \
                                               + " (id,name,test_case,data,tools,nextid,expected,test_explain) values " \
                                               + "('" + str(case_id) + "', '" \
                                               + str(name) + "', '" \
                                               + str(case) + "', '" \
                                               + str(data) + "', '" \
                                               + str(tools) + "', '" \
                                               + str(nextid) + "', '" \
                                               + str(expected) + "', '" \
                                               + str(explain) + "');"
                            cursor.execute(sql_insert_table)
                            database.commit()

                    print "over"
                    cursor.close()
                    database.close()

                    return render(request, 'Up_load.html', context)
                else:
                    # return HttpResponse('文件类新错误,重新选择')
                    context = {'prompt': '文件类型错误,请重新选择'}
                    return render(request, 'Up_load.html', context)
    else:
        return render(request, 'Up_load.html')


def show_progress(request):
    return JsonResponse({"result": str(num_process)})


def upload_mailaddress(request):
    if request.method == 'POST':
        # 接受传递过来的数据并存到数据库中
        post = request.POST
        mailsite = post.get('mailsite')
        namesite = post.get('namesite')
        try:
            mysql_db.Mail.objects.get(mailaddress=mailsite)
            selectall = mysql_db.Mail.objects.all()
            return render(request, 'upload_mailaddress.html', {'result': selectall, "valid": "2"})
        except:
            sql = mysql_db.Mail()
            sql.mailaddress = mailsite
            sql.username = namesite
            sql.asr_state = '0'
            sql.nlu_state = '0'
            sql.save()
            # 从数据库取出数据显示到页面中去
            selectall = mysql_db.Mail.objects.all()
            return render(request, 'upload_mailaddress.html', {'valid': '1', 'result': selectall})

    else:
        selectall = mysql_db.Mail.objects.all()
        return render(request, 'upload_mailaddress.html', {'result': selectall})


def upload_mailaddress_del(request, uname):
    user = mysql_db.Mail.objects.filter(username=uname)
    if user:
        user.delete()
        return redirect("/uploadmail/")
    else:
        return HttpResponse('删除失败')


def mail_task(request):
    state_1 = mysql_db.Mail.objects.filter(asr_state='1')
    state_2 = mysql_db.Mail.objects.filter(nlu_state='1')
    state_3 = mysql_db.Mail.objects.filter(nlp_state='1')
    selectall = mysql_db.Mail.objects.all()
    return render(request,'mail_task.html',{'state1':state_1,'state2':state_2,'state3':state_3,
                                            'result':selectall})


def mail_task_handle(request):
    if request.method == 'POST':
        post = request.POST
        if post.has_key('asrname'):
            namelist = post.getlist('asrname')
            mysql_db.Mail.objects.all().update(asr_state='0')
            for i in namelist:
                i = i.strip("/")
                try:
                    valid = mysql_db.Mail.objects.get(username=i)
                except:
                    continue
                if valid:
                    valid.asr_state = '1'
                    valid.save()

        if post.has_key('nluname'):
            namelist = post.getlist('nluname')
            mysql_db.Mail.objects.all().update(nlu_state='0')
            for i in namelist:
                i = i.strip("/")
                try:
                    valid = mysql_db.Mail.objects.get(username=i)
                except:
                    continue
                if valid:
                    valid.nlu_state = '1'
                    valid.save()

        if post.has_key('nlpname'):
            namelist = post.getlist('nlpname')
            mysql_db.Mail.objects.all().update(nlp_state='0')
            for i in namelist:
                i = i.strip("/")
                try:
                    valid = mysql_db.Mail.objects.get(username=i)
                except:
                    continue
                if valid:
                    valid.nlp_state = '1'
                    valid.save()

        selectall = mysql_db.Mail.objects.all()
        return render(request, 'mail_task.html', {'result': selectall})





