# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from public_methods import set_logger
from django.views.decorators.csrf import csrf_exempt
from apps.testservice.views.public_methods import nlpurl_valid
import super_around
import threading
import time
import json

# 设置python的递归层数
import sys
sys.setrecursionlimit(1000000)
test_wait = False


@csrf_exempt
def test_listner(request):
    logger = set_logger()
    try:
        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if request.method == 'POST':
            try:
                post = request.POST
                version = post.get('version')
                if version is None:
                    print request.POST["param"]
                    param = json.loads(request.POST["param"])
                    # ------------------------------------
                    caseid = param['caseId']
                    urls = param['url']
                    print param
                    # nlpurl验证
                    caseid_cut = caseid.split("_")[0]
                    if caseid_cut == "nlp" and urls != "":
                        nlpurl_valid(urls)
                    param.setdefault('start_time', (str(start_time)))
                    t = create_threading(param)
                    t.start()
                else:
                    caseid = post.get('caseid')
                    tablename = post.get('tablename')
                    times = post.get('times')
                    urls = post.getlist('url')
                    url_dict = {}
                    mail_valid = post.get("mail_valid")
                    sheet_name = post.get("sheetname")
                    for i in range(len(urls)):
                        url = urls[i]
                        if url == "":
                            continue
                        url_dict.setdefault('url'+str(i+1), url)

                    # nlpurl验证
                    caseid_cut = caseid.split("_")[0]
                    if caseid_cut == "nlp" and url_dict != {}:
                        # 声明一个变量用于阻塞其他测试
                        global test_wait
                        test_wait = True
                        nlpurl_valid(url_dict)
                        test_wait = False
                    param = {'version': version, 'caseId': caseid, 'tableName': tablename,
                             'times': times, 'url': url_dict, "start_time": str(start_time),
                             "mail_valid": mail_valid, "sheet_name": sheet_name, "test_wait": test_wait}
                    print param
                    t = create_threading(param)
                    t.start()
            except Exception as e:
                print e
                print request.POST["param"]
                t = create_threading(request.POST["param"])
                t.start()

        return redirect("/test/")
    except:
        logger.exception("Exception Logged")


def create_threading(param):
    p = [param]
    print "new threading"
    new_threading = threading.Thread(target=super_around.super_around, args=p)
    return new_threading

