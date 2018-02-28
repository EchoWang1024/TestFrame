# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.testservice import models as mysql_db

from django.shortcuts import render, redirect, HttpResponse
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse
import os
import MySQLdb
# Create your views here.


def test_case(request, p_index):
    if request.method == 'GET':
        valid = request.GET.get('valid')
    list = mysql_db.TestPath.objects.order_by("-id")
    p = Paginator(list, 8)
    if p_index == '':
        p_index = '1'
    list2 = p.page(int(p_index))
    plist = p.page_range
    plast = ''
    plast2 = ''
    if plist[-1] > 5:
        plast = plist[-1]
        plast2 = plist[-2]
    context = {'list': list2, 'plist': plist, 'Pindex': int(p_index), 'plast': plast, 'plast2': plast2, 'valid': valid}
    return render(request, 'Test_case.html', context)


def test_case_handle(request, Pindex):

    if request.method == 'POST':
        post = request.POST
        table_name = post.get('table_name')
        global user
        user = mysql_db.TestPath.objects.filter(table_name=table_name)
        if len(user) == 0:
            return HttpResponseRedirect('/test_case1/?valid=0')
        else:
            list = user.order_by("-id")
            p = Paginator(list, 8)
            if Pindex == '':
                Pindex = '1'
            Pindex = int(Pindex)
            list2 = p.page(Pindex)
            plist = p.page_range
            plast = ''
            plast2 = ''
            if plist[-1] > 5:
                plast = plist[-1]
                plast2 = plist[-2]
            context = {'list': list2, 'plist': plist, 'Pindex': Pindex, 'plast': plast, 'plast2': plast2, 'valid': '1'}
            return render(request, 'Test_case.html', context)
    else:
        try:
            list = user.order_by("-id")
        except:
            list = mysql_db.TestPath.objects.order_by("-id")
        p = Paginator(list, 8)
        if Pindex == '':
            Pindex = '1'
        Pindex = int(Pindex)
        list2 = p.page(Pindex)
        plist = p.page_range
        plast = ''
        plast2 = ''
        if plist[-1] > 5:
            plast = plist[-1]
            plast2 = plist[-2]
        context = {'list': list2, 'plist': plist, 'Pindex': Pindex, 'plast': plast, 'plast2': plast2, 'valid': '1'}
        return render(request, 'Test_case.html', context)


def test_case_download(request, case):

    valid = mysql_db.TestPath.objects.filter(table_name=case)
    table_path = valid[0].table_path
    table_path1 = table_path + '/' + case

    try:
        def file_iterator(file_name, chunk_size=512):
                with open(file_name) as f:
                    while True:
                        c = f.read(chunk_size)
                        if c:
                            yield c
                        else:
                            break
    except:
        return HttpResponse('文件不存在')

    the_file_name = table_path1
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(case)
    return response


def test_case_del(request, table_name):

    # del sql
    try:
        sql_table_name = table_name.split(".")[0]
        database = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="test", charset="utf8")
        cursor = database.cursor()
        sql_table_drop = "drop table " + sql_table_name
        cursor.execute(sql_table_drop)
        cursor.close()
        database.close()
    except Exception as e:
        print str(e) + "数据表不存在"

    # del xlsx
    valid = mysql_db.TestPath.objects.filter(table_name=table_name)
    path = valid[0].table_path+'/'
    path_name = path + table_name
    if valid:
        os.remove(path_name)
        valid.delete()
        return redirect("/test_case1/")


def test_case_del_most(request):
    print request.method
    if request.method == "POST":
        post = request.POST
        table_name_list = post.getlist("table_name")
        if len(table_name_list) == 0:
            return redirect("/test_case1/")
        for table_name in table_name_list:
            try:
                sql_table_name = table_name.split(".")[0]
                database = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="test", charset="utf8")
                cursor = database.cursor()
                sql_table_drop = "drop table " + sql_table_name
                cursor.execute(sql_table_drop)
                cursor.close()
                database.close()
            except Exception as e:
                print str(e) + "数据表不存在"

            valid = mysql_db.TestPath.objects.filter(table_name=table_name)
            path = valid[0].table_path + '/'
            path_name = path + table_name
            if valid:
                os.remove(path_name)
                valid.delete()
        return redirect("/test_case1/")




