# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.testservice import models as mysql_db
from django.shortcuts import render,redirect
from django.http import JsonResponse
import xlrd
import os
# Create your views here.


def home(request):
    return render(request, 'home.html')


def home_handle(request):
    print request.method
    os.system("iconv -f utf-8 -ct gbk /part/home/pachiratest/mylog/TestFrame_log.txt"
              " > TestFrame_log_gbk.txt")
    return redirect("http://192.168.128.54/mylog/TestFrame_log.txt")


def execution_test(request):
    table = mysql_db.TestPath.objects.order_by("-id")
    return render(request, 'Execution_test.html', {"table": table})


def execution_test_5(request):
    return render(request, '5.0_Execute_test.html')


def table_valid(request):
    tablename = request.GET.get('tablename')
    result = mysql_db.TestPath.objects.filter(table_name=tablename).count()
    context = {'result': result}
    return JsonResponse(context)


def sheet_valid(request):
    ajax_get = request.GET
    table_name = ajax_get.get("table_name")
    table_path = mysql_db.TestPath.objects.filter(table_name=table_name)[0].table_path
    select_path = table_path + '/' + table_name
    book = xlrd.open_workbook(select_path)
    result = []
    for sheet in book.sheets():
        result.append(str(sheet.name))
    context = {"result": result}
    return JsonResponse(context)


def caseid_valid(request):
    case = request.GET
    tablename = case.get('tablename')
    caseid = case.get('caseid')
    tablepath = mysql_db.TestPath.objects.filter(table_name=tablename)[0].table_path
    selectpath = tablepath + '/' + tablename
    book = xlrd.open_workbook(selectpath)
    sheet0 = book.sheet_by_index(0)
    col_data1 = sheet0.col_values(0)
    result = 0
    for i in col_data1:
        if caseid == i:
            result = 1
    context = {'result': result}
    return JsonResponse(context)


