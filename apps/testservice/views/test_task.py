# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.testservice import models as mysql_db
# 导入分页方法
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import HttpResponseRedirect
# 导入Q方法,用于多条件查询
from django.db.models import Q
# Create your views here.


def test_task(request, Pindex):
    if request.method == 'GET':
        valid = request.GET.get('valid')
    list1 = mysql_db.TestFrame.objects.order_by('-id')
    p = Paginator(list1, 15)
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
    return render(request, 'Test_task.html', {'list': list2, 'plist': plist, 'Pindex': Pindex, 'valid': valid,
                                              'plast': plast, 'plast2': plast2})


def test_task_handle(request, Pindex):
    if request.method == 'POST':
        post = request.POST
        test_id = post.get('test_id')
        case_id = post.get('case_id')
        version_num = post.get('version_num')
        entry_name = post.get('entry_name')
        table_name = post.get('table_name')
        state = post.get('state')

        di = {}
        if test_id != "":
            di.setdefault('test_id', test_id)
        if case_id != "":
            di.setdefault('case_id', case_id)
        if version_num != "":
            di.setdefault('version_num', version_num)
        if entry_name != "":
            di.setdefault('entry_name', entry_name)
        if table_name != "":
            di.setdefault('table_name', table_name)
        if state != "":
            di.setdefault('state', state)
        global q
        q = Q()
        for i in di:
            q.add(Q(**{i: di[i]}), Q.AND)
        print q
        user = mysql_db.TestFrame.objects.filter(q)
        print user
        if len(user) == 0:
            return HttpResponseRedirect('/test_task1/?valid=0')
        else:
            list2 = user.order_by('-id')
            p = Paginator(list2, 15)
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
            return render(request, 'Test_task.html', {'list': list2, 'plist': plist, 'Pindex': Pindex,
                                                      'valid': '1', 'plast': plast, 'plast2': plast2})

    else:
        try:
            user = mysql_db.TestFrame.objects.filter(q)
            list2 = user.order_by('-id')
        except:
            list2 = mysql_db.TestFrame.objects.order_by('-id')
        p = Paginator(list2, 15)
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
        return render(request, 'Test_task.html', {'list': list2, 'plist': plist, 'Pindex': Pindex, 'valid': '1',
                                                  'plast': plast, 'plast2': plast2})
        # return render(request, 'Test_task.html')


def test_task_download(request, index):
    valid = mysql_db.ResultPath.objects.filter(test_id=index)
    result_path = valid[0].result_path

    download_path = result_path + '_gbk.txt'
    file_name = result_path.split('/')[-1] + '_gbk.txt'

    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(download_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response


def nlp_flog_download(request, index):
    valid = mysql_db.ResultPath.objects.filter(test_id=index)
    result_path = valid[0].result_path
    download_path = result_path + '_flog.txt'
    file_name = result_path.split('/')[-1] + '_flog.txt'

    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(download_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response


def test_task_nludownload(request, index):
    valid = mysql_db.ResultPath.objects.filter(test_id=index)
    result_path = valid[0].result_path

    download_path = result_path + '_out.xml'
    file_name = result_path.split('/')[-1] + '_out.xml'

    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(download_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response


