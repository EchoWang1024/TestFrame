#!/usr/bin/env Python
# coding=utf-8

from apps.testservice import models as mysql_db
import public_methods
import os
import re
import time


def hawkdecoder_result(test_result_file, test_id, message, expected, report_folder, count, explain):

    global test_result

    test_result_file = open(test_result_file, "rw")
    lines = test_result_file.readlines()

    rate = lines[6].split("|")[3].split(" ")[1]

    counts = '第' + str(count) + '轮测试'

    if rate >= expected:
        test_result = 'success'
    else:
        test_result = "false"

    print lines

    print test_result
    print test_id
    print message["caseId"]

    report_file = report_folder+"/"+test_id+"report.txt"
    report_file_gbk = report_folder + "/" + test_id + "report_gbk.txt"

    try:
        os.system("touch " + report_folder + "/" + test_id + "report.txt")
        o_report_file = open(report_file, "a")
        o_report_file.write(explain)
        o_report_file.write("\n")
        o_report_file.write("--------------------------------" + test_id + ' ' + str(count)
                            + "----------------------------------")

    except:

        o_report_file = open(report_file, "a")

    o_report_file.write("\n")
    o_report_file.write(message["caseId"]+test_result)
    o_report_file.write("\n")
    o_report_file.write(counts)
    o_report_file.write("\n")
    o_report_file.write("句正确率:"+rate)
    o_report_file.write("\n")
    for i in range(1, len(lines)):
        o_report_file.write(lines[i])

    o_report_file.close()
    os.system("iconv -c -f utf-8 -t gbk " + report_file + " >" + report_file_gbk)
    print "iconv -c -f utf-8 -t gbk " + report_file + " >" + report_file_gbk


def nlutest_result(test_result_file, test_id, message, report_folder, explain):
    pwd = os.getcwd()
    print pwd
    global test_result

    test_result_file = open(test_result_file, "rw")
    lines = test_result_file.readlines()
    falses = 0
    trues = 0

    for line in lines:
        if line[-2] == '1':
            falses = falses + 1
        else:
            trues = trues + 1
    if falses > 0:
        test_result = "false"
    else:
        test_result = "true"

    sums = falses + trues
    print "---------------------"+str(sums)+","+str(trues)
    valid = str(float(trues)/sums)

    excepted = "0"

    report_file = report_folder + "/" + test_id + "report.txt"
    report_file_gbk = report_folder + "/" + test_id + "report_gbk.txt"
    try:
        os.system("touch " + report_folder + "/" + test_id + "report.txt")
        public_methods.insert_table(test_id, report_folder + "/" + test_id + "report", "resultPath", "")
        o_report_file = open(report_file, "a")
        o_report_file.write(explain)
        o_report_file.write("\n")
        o_report_file.write("--------------------------------" + test_id + "----------------------------------")

    except:

        o_report_file = open(report_file, "a")

    o_report_file.write("\n")
    o_report_file.write(message["caseId"] + ' -- ' + test_result)
    o_report_file.write("\n")
    o_report_file.write("期望值:" + ' ' + excepted)
    o_report_file.write("\n")
    o_report_file.write("正确率:" + ' ' + str(valid))
    o_report_file.write("\n")
    o_report_file.write("正确个数: " + str(trues) + ' ' + "失败个数:" + str(falses))
    o_report_file.write("\n\n")
    o_report_file.write("错误的有:")
    o_report_file.write("\n")
    for line in lines:
        if line[-2] == '1':
            o_report_file.write(line)

    o_report_file.close()

    os.system("iconv -f utf-8 -t gbk " + report_file + " >" + report_file_gbk)


def nlptest_result(test_id, explain, casepath, count, case_id, flog, test_result_file):

    logger, fh, ch = public_methods.set_logger()
    '''统计一次测试完成后成功和失败的个数　true_count ; faile_count '''
    true_count = 0
    faile_count = 0
    # 统计轮测试数
    counts = '第' + str(count) + '轮测试'
    # 打开结果文件,计算正确和错误
    compare_result = open(casepath + "/test/compare_result.txt", "r")
    for line in compare_result:
        if "测试成功" in line:
            true_count += 1
        elif "测试失败" in line:
            faile_count += 1
    compare_result.close()
    # 将本次测试结果记录到log
    if faile_count == 0:
        logger.info(counts + " 用例:" + case_id + "测试成功")
    else:
        logger.info(counts + " 用例:" + case_id + "测试失败")

    '''执行之后将其中的错误的报告写入到文件中'''
    return_fail = open(casepath + "/test/return_result_fail.txt")
    flog.write(return_fail.read())
    return_fail.close()

    # 获取nlp－count数据库4
    try:
        nlp_count = mysql_db.NlpCount.objects.get(test_id=test_id, count=str(count))
    except Exception as e:
        print e
        nlp_valid = mysql_db.NlpCount(test_id=test_id, count=count, nlp_true=0, nlp_fail=0)
        nlp_valid.save()
        nlp_count = mysql_db.NlpCount.objects.get(test_id=test_id, count=str(count))

    # 用例测试成功--成功将记录到数据库成功个数取出并增加
    if faile_count == 0:
        nlp_count.nlp_true += 1
        nlp_count.save()

    # 用例测试失败--成功将记录到数据库成功个数取出并增加
    elif faile_count != 0:
        nlp_count.nlp_fail += 1
        nlp_count.save()

    # 正则表达式选取错误结果写入报告
    compare_result = open(casepath + "/test/compare_result.txt", "r")
    result_read = compare_result.read()
    result = re.findall(">>>[\s\S]*?<<<", str(result_read))

    '''－－－－－－－－－－－－开始进行报告整理－－－－－－－－－－－－－'''

    if "测试失败" in result_read:

        test_result_file.write("\n")
        test_result_file.write("-------------------------------------------------------"
                               + str(case_id)
                               + "--------------------------------------------------")
        test_result_file.write("\n")
        test_result_file.write("说明 : " + explain)
        test_result_file.write("\n")
        test_result_file.write("结果 : " + str(case_id) + counts + "失败")
        test_result_file.write("\n")
        test_result_file.write("正确个数为 : " + str(true_count) + '    ' + "失败个数为 : " + str(faile_count))
        test_result_file.write("\n")
        test_result_file.write("测试失败的字段如下 : ")

    for i in result:
        if "测试失败" in i:
            test_result_file.write("\n")
            test_result_file.write(i)
            test_result_file.write("\n")

    compare_result.close()


'''pstt'''


def pstt_asr_report(case_id, count, explain, test_refs, pstt_result, prt, drt, cpu, regs, wav_name, run_time):

    test_refs = eval(test_refs)
    pstt_result.write("－－－－ >> case_id : " + case_id + "\n"
                      + "\n 说明 : " + explain
                      + "\n 测试类型 : pstt - asr"
                      + "\n 测试时间 : " + str(run_time) + "秒"
                      + "\n 音频文件 : " + wav_name
                      + "\n 内存占用 : " + cpu
                      + "\n 执行速度 : { prt : " + prt + " drt : " + drt + " }"
                      + "\n 期待执行速度 : { prt : " + test_refs["rt"]["prt"] + " brt : " + test_refs["rt"]["drt"] + " }\n"
                      + "\n 识别率信息如下 : ↓\n" + str(regs[0]) + str(regs[1]) + str(regs[2]) + str(regs[3]) + str(regs[4])
                      + "\n 期待识别率如下 : ↓\n")
    pstt_result.write(
        " ----------------------------------------------------------------------------------------------------- \n"
        + "|   PASR     |     Snt        Wrd   |   Corr        Sub        Del        Ins        Err      S.Err   |\n"
        + " ----------------------------------------------------------------------------------------------------- \n"
        + "|  Sum/Avg   |" + test_refs["Snt"].center(11) + test_refs["Wrd"].center(11) + "|"
        + test_refs["Corr"].center(11) + test_refs["Sub"].center(11) + test_refs["Del"].center(11)
        + test_refs["Ins"].center(11) + test_refs["Err"].center(11) + test_refs["S.Err"].center(10) + "|\n"
        + " ----------------------------------------------------------------------------------------------------- \n\n")
    # rt对比
    if prt >= test_refs["rt"]["prt"] and drt >= test_refs["rt"]["drt"]:
        rt_valid = True
    else:
        rt_valid = False
    # 识别率对比
    reg_refs = [test_refs["Snt"], test_refs["Wrd"], test_refs["Corr"], test_refs["Sub"], test_refs["Del"],
                test_refs["Ins"], test_refs["Err"], test_refs["S.Err"]]
    reg_line = str(regs[3])
    reg_result = re.findall("(\d+(\.\d+)?)", reg_line)
    reg_valid = 0
    for x, y in zip(reg_refs, reg_result):
        if float(x) > float(y[0]):
            reg_valid += 1
    if reg_valid == 0 and rt_valid is True:
        pstt_result.write("测试结果 : " + case_id + "第" + count + "轮测试成功\n\n")
    else:
        pstt_result.write("测试结果 : " + case_id + "第" + count + "轮测试失败\n\n")
    # pstt_result.close()
    print "pstt report ok!!!!"


def pstt_spk_report(case_id, count, explain, test_refs, pstt_result, prt, drt, cpu, regs, wav_name, speaker, main_path,
                    run_time, spk_der):

    test_refs = eval(test_refs)
    pstt_result.write("－－－－ >> case_id : " + case_id + "\n"
                      + "\n 说明 : " + explain
                      + "\n 测试类型 : pstt - spk"
                      + "\n 测试时间 : " + str(run_time) + "秒"
                      + "\n 音频文件 : " + wav_name
                      + "\n 内存占用 : " + str(cpu)
                      + "\n 说话人 : " + speaker
                      + "\n 正确说话人 : A,B "
                      + "\n 执行速度 : { prt : " + str(prt) + " drt : " + str(drt) + " }"
                      + "\n 期待执行速度 : { prt : " + str(test_refs["rt"]["prt"])
                      + " brt : " + str(test_refs["rt"]["drt"]) + " }\n")
    pstt_result.write(
        "\n 识别率信息如下 : ↓\n" + str(regs[0]) + str(regs[1]) + str(regs[2]) + str(regs[3]) + str(regs[4])
        + " 期待识别率如下 : ↓\n"
        + " ----------------------------------------------------------------------------------------------------- \n"
        + "|   PASR     |     Snt        Wrd   |   Corr        Sub        Del        Ins        Err      S.Err   |\n"
        + " ----------------------------------------------------------------------------------------------------- \n"
        + "|  Sum/Avg   |" + test_refs["Snt"].center(11) + test_refs["Wrd"].center(11) + "|"
        + test_refs["Corr"].center(11) + test_refs["Sub"].center(11) + test_refs["Del"].center(11)
        + test_refs["Ins"].center(11) + test_refs["Err"].center(11) + test_refs["S.Err"].center(10) + "|\n"
        + " ----------------------------------------------------------------------------------------------------- \n\n")
    # 时间边界验证(单句)
    pstt_result.write("时间边界验证(单句)，错误结果如下 : ↓\n\n")
    with open(main_path + "pstt_result.txt", "r") as f:
        for line in f.readlines():
            speak_time = re.findall("\([\s\S]*?\)", line)
            valid = "0"
            for i in speak_time:
                if int(valid) > int(i.split("/")[0].split("-")[-1]):
                    pstt_result.write(line)
                    break
                else:
                    valid = i.split("/")[0].split("-")[-1]
    # 时间边界验证(上下句)
    pstt_result.write("时间边界验证(上下句)，错误结果如下 : ↓\n\n")
    with open(main_path + "pstt_result.txt", "r") as f:
        previous_line = ""
        valid = "0"
        for line in f.readlines():
            # 首先判断上下句是否是同一音频
            pre_wav = previous_line.split("/")[-1].split(".")[0]
            line_wav = line.split("/")[-1].split(".")[0]
            if pre_wav == line_wav:
                line_spk_time = re.findall("\[[\s\S]*?\]", line)
                line_valid_time = line_spk_time[0].split("-")[-1][:-1]
                if int(valid) > int(line_valid_time):
                    pstt_result.write(previous_line)
                    pstt_result.write(line)
                previous_line = line
                valid = line_valid_time
            else:
                previous_line = ""
                valid = "0"
    # Der值判断并写入：
    if spk_der == "":
        pstt_result.write(
            "der值对比结果如下 : ↓\n\n"
            + " -----------------------------------------------------------------------------------------------------\n"
            + " |    keyword    |              der-result                 |              der-except                  |\n"
            + " -----------------------------------------------------------------------------------------------------\n"
        )
        der_list = []
        with open(main_path + "../spk_tools/result/total_log.txt", "r") as f:
            for line in f.readlines():
                der_list.append(line)
        der_rt = der_list[-1].strip()
        der = der_list[-4]
        der_t = round(float(der.split("-")[-1].split("(")[0].strip()), 2)
        der_m = round(float(der.split("-")[0].split(",")[0].split("(")[0].strip()), 2)
        der_f = round(float(der.split("-")[0].split(",")[1].split("(")[0].strip()), 2)
        der_s = round(float(der.split("-")[0].split(",")[-1].split("(")[0].strip()), 2)
        pstt_result.write(
            " |       M       |" + str(der_m).center(41) + "|" + test_refs["der"]["M"].center(42) + "| \n"
            + " -----------------------------------------------------------------------------------------------------\n"
            + " |       F       |" + str(der_f).center(41) + "|" + test_refs["der"]["F"].center(42) + "| \n"
            + " -----------------------------------------------------------------------------------------------------\n"
            + " |       S       |" + str(der_s).center(41) + "|" + test_refs["der"]["S"].center(42) + "| \n"
            + " -----------------------------------------------------------------------------------------------------\n"
            + " |       T       |" + str(der_t).center(41) + "|" + test_refs["der"]["T"].center(42) + "| \n"
            + " -----------------------------------------------------------------------------------------------------\n"
            + " |      RT       |" + str(der_rt).center(41) + "|" + test_refs["der"]["RT"].center(42) + "| \n"
            + " -----------------------------------------------------------------------------------------------------\n"
        )
        der = False
        if (der_m < float(test_refs["der"]["M"]) and der_f < float(test_refs["der"]["F"])
            and der_s < float(test_refs["der"]["S"]) and der_t < float(test_refs["der"]["T"])
                and der_rt < float(test_refs["der"]["RT"])):
            der = True
    # speaker判断
    if speaker == "A,B":
        speaker_valid = True
    else:
        speaker_valid = False
    # rt对比
    if prt >= test_refs["rt"]["prt"] and drt >= test_refs["rt"]["drt"]:
        rt_valid = True
    else:
        rt_valid = False
    # 识别率对比
    reg_refs = [test_refs["Snt"], test_refs["Wrd"], test_refs["Corr"], test_refs["Sub"], test_refs["Del"],
                test_refs["Ins"], test_refs["Err"], test_refs["S.Err"]]
    reg_line = str(regs[3])
    reg_result = re.findall("(\d+(\.\d+)?)", reg_line)
    reg_valid = 0
    for x, y in zip(reg_refs, reg_result):
        if float(x.strip()) > float(y[0].strip()):
            reg_valid += 1
    if spk_der == "":
        if reg_valid == 0 and rt_valid is True and speaker_valid is True:
            pstt_result.write("测试结果 : " + case_id + "第" + count + "轮测试成功")
        else:
            pstt_result.write("测试结果 : " + case_id + "第" + count + "轮测试失败")
    else:
        if reg_valid == 0 and rt_valid is True and speaker_valid is True and der is True:
            pstt_result.write("测试结果 : " + case_id + "第" + count + "轮测试成功\n\n")
        else:
            pstt_result.write("测试结果 : " + case_id + "第" + count + "轮测试失败\n\n")
    # pstt_result.close()
    print "pstt report ok!!!!"


def pstt_spkem_report(case_id, count, explain, test_refs, pstt_result, prt, drt, cpu, regs, wav_name, speaker,
                      main_path, run_time, emo):

    test_refs = eval(test_refs)
    pstt_result.write("－－－－ >> case_id : " + case_id + "\n"
                      + "\n 说明 : " + explain
                      + "\n 测试类型 : pstt - spk"
                      + "\n 测试时间 : " + str(run_time) + "秒"
                      + "\n 音频文件 : " + wav_name
                      + "\n 内存占用 : " + str(cpu)
                      + "\n 说话人 : " + speaker
                      + "\n 正确说话人 : A,B "
                      + "\n 说话情绪 : " + emo
                      + "\n 参考说话情绪 : Neu Ag Unk"
                      + "\n 执行速度 : { prt : " + str(prt) + " drt : " + str(drt) + " }"
                      + "\n 期待执行速度 : { prt : " + str(test_refs["rt"]["prt"])
                      + " brt : " + str(test_refs["rt"]["drt"]) + " }\n")
    pstt_result.write(
        "\n 识别率信息如下 : ↓\n" + str(regs[0]) + str(regs[1]) + str(regs[2]) + str(regs[3]) + str(regs[4])
        + " 期待识别率如下 : ↓\n"
        + " ----------------------------------------------------------------------------------------------------- \n"
        + "|   PASR     |     Snt        Wrd   |   Corr        Sub        Del        Ins        Err      S.Err   |\n"
        + " ----------------------------------------------------------------------------------------------------- \n"
        + "|  Sum/Avg   |" + test_refs["Snt"].center(11) + test_refs["Wrd"].center(11) + "|"
        + test_refs["Corr"].center(11) + test_refs["Sub"].center(11) + test_refs["Del"].center(11)
        + test_refs["Ins"].center(11) + test_refs["Err"].center(11) + test_refs["S.Err"].center(10) + "|\n"
        + " ----------------------------------------------------------------------------------------------------- \n\n")
    # 时间边界验证(单句)
    pstt_result.write("时间边界验证(单句)，错误结果如下 : ↓\n\n")
    with open(main_path + "pstt_result.txt", "r") as f:
        for line in f.readlines():
            speak_time = re.findall("\([\s\S]*?\)", line)
            valid = "0"
            for i in speak_time:
                if int(valid) > int(i.split("/")[0].split("-")[-1]):
                    pstt_result.write(line)
                    break
                else:
                    valid = i.split("/")[0].split("-")[-1]
    # 时间边界验证(上下句)
    pstt_result.write("时间边界验证(上下句)，错误结果如下 : ↓\n\n")
    with open(main_path + "pstt_result.txt", "r") as f:
        previous_line = ""
        valid = "0"
        for line in f.readlines():
            # 首先判断上下句是否是同一音频
            pre_wav = previous_line.split("/")[-1].split(".")[0]
            line_wav = line.split("/")[-1].split(".")[0]
            if pre_wav == line_wav:
                line_spk_time = re.findall("\[[\s\S]*?\]", line)
                line_valid_time = line_spk_time[0].split("-")[-1][:-1]
                if int(valid) > int(line_valid_time):
                    pstt_result.write(previous_line)
                    pstt_result.write(line)
                previous_line = line
                valid = line_valid_time
            else:
                previous_line = ""
                valid = "0"
    # speaker判断
    if speaker == "A,B":
        speaker_valid = True
    else:
        speaker_valid = False
    # rt对比
    if prt >= test_refs["rt"]["prt"] and drt >= test_refs["rt"]["drt"]:
        rt_valid = True
    else:
        rt_valid = False
    # 识别率对比
    reg_refs = [test_refs["Snt"], test_refs["Wrd"], test_refs["Corr"], test_refs["Sub"], test_refs["Del"],
                test_refs["Ins"], test_refs["Err"], test_refs["S.Err"]]
    reg_line = str(regs[3])
    reg_result = re.findall("(\d+(\.\d+)?)", reg_line)
    reg_valid = 0
    for x, y in zip(reg_refs, reg_result):
        if float(x.strip()) > float(y[0].strip()):
            reg_valid += 1
    if reg_valid == 0 and rt_valid is True and speaker_valid is True and emo != "None":
        pstt_result.write("测试结果 : " + case_id + "第" + count + "轮测试成功\n\n")
    else:
        pstt_result.write("测试结果 : " + case_id + "第" + count + "轮测试失败\n\n")
    # pstt_result.close()
    print "pstt report ok!!!!"


def pstt_asrone_report(case_id, count, explain, test_refs, pstt_result, cpu, regs, wav_name, speaker,
                       main_path, run_time):

    test_refs = eval(test_refs)
    result_answer = ""
    result_vt = ""
    result_log = ""
    with open(main_path + "../client/result_one.txt", "r") as f:
        f_line = f.readlines()
        for line in f_line:
            if "(0)" in line:
                result_answer = line.split("[")[-1].split("(")[0]
                # print result_answer
            if "Voice Time" in line:
                result_vt = line.split(":")[-1].strip()
            if "Log" in line:
                result_log = line.split(":")[-1].strip()

    pstt_result.write(
        "－－－－ >> case_id : " + case_id + "\n"
        + "\n 说明 : " + explain
        + "\n 测试类型 : pstt-asr-one"
        + "\n 测试时间 : " + str(run_time) + "秒"
        + "\n 音频文件 : " + wav_name
        + "\n 内存占用 : " + str(cpu)
        + "\n LogId : " + result_log
        + "\n LogId/16 : " + str(float(result_log)/16)
        + "\n VoiceTime : " + result_vt
        + "\n Answer : " + result_answer.decode("gbk")
        + "\n ExceptAnswer : " + test_refs["answer"] + "\n"
    )
    # 执行对比
    if result_answer == test_refs["answer"]:
        pstt_result.write(" 测试结果 : " + case_id + "第" + count + "轮测试成功\n\n")
    else:
        pstt_result.write(" 测试结果 : " + case_id + "第" + count + "轮测试失败\n\n")


def pstt_spkone_report(case_id, count, explain, test_refs, pstt_result, cpu, regs, wav_name, speaker,
                       main_path, run_time):

    test_refs = eval(test_refs)
    result_vt = ""
    result_log = ""
    with open(main_path + "../client/result_one.txt", "r") as f:
        f_line = f.readlines()
    with open(main_path + "../client/result_one.txt", "r") as f:
        f_read = f.read()
    for line in f_line:
        if "Voice Time" in line:
            result_vt = line.split(":")[-1].strip()
        if "Log" in line:
            result_log = line.split(":")[-1].strip()

    # 说话人验证
    if "A[" in f_read and "B[" not in f_read:
        speaker = "A"
    if "A[" not in f_read and "B[" in f_read:
        speaker = "B"
    if "A[" in f_read and "B[" in f_read:
        speaker = "A B"
    # answer验证
    tim_rim = (re.findall("sult:[\s\S]*?Sum", f_read)[0][4:-3]).split("\n")
    del tim_rim[0]
    del tim_rim[-1]
    answer = ""
    for x in tim_rim:
        speak = x.split(":")[-1].split("(")[0]
        answer += speak.decode("gbk", "ignore")

    pstt_result.write(
        "－－－－ >> case_id : " + case_id + "\n"
        + "\n 说明 : " + explain
        + "\n 测试类型 : pstt-asr-one"
        + "\n 测试时间 : " + str(run_time) + "秒"
        + "\n 音频文件 : " + wav_name
        + "\n 内存占用 : " + str(cpu)
        + "\n LogId : " + result_log
        + "\n LogId/16 : " + str(float(result_log)/16)
        + "\n VoiceTime : " + result_vt
        + "\n Answer : " + answer
        + "\n ExceptAnswer : " + test_refs["answer"]
        + "\n Speaker : " + speaker
        + "\n ExceptSpeaker : A B \n"
    )
    # 时间边界验证(单句)

    pstt_result.write(" 时间边界验证(单句)，错误结果如下 : ↓\n\n")

    for line in tim_rim:
        line = line.split(":")[-1]
        print line
        speak_time = re.findall("\([\s\S]*?\)", line)
        valid = "0"
        for i in speak_time:
            if int(valid) > int(i.split("/")[0].split("-")[-1]):
                pstt_result.write(line)
                break
            else:
                valid = i.split("/")[0].split("-")[-1]

    # 时间边界验证(上下句)
    pstt_result.write(" 时间边界验证(上下句)，错误结果如下 : ↓\n\n")
    previous_line = ""
    valid = "0"
    for line in tim_rim:
        line_spk_time = re.findall("\[[\s\S]*?\]", line)
        line_valid_time = line_spk_time[0].split("-")[-1][:-1]
        if int(valid) > int(line_valid_time):
            pstt_result.write(previous_line)
            pstt_result.write(line)
        previous_line = line
        valid = line_valid_time

    # 执行对比
    if answer == test_refs["answer"] and speaker == "A B":
        pstt_result.write(" 测试结果 : " + case_id + "第" + count + "轮测试成功\n\n")
    else:
        pstt_result.write(" 测试结果 : " + case_id + "第" + count + "轮测试失败\n\n")


def pstt_emoone_report(case_id, count, explain, test_refs, pstt_result, cpu, regs, wav_name, speaker,
                       main_path, run_time):

    test_refs = eval(test_refs)
    result_vt = ""
    result_log = ""
    with open(main_path + "../client/result_one.txt", "r") as f:
        f_line = f.readlines()
    with open(main_path + "../client/result_one.txt", "r") as f:
        f_read = f.read()
    for line in f_line:
        if "Voice Time" in line:
            result_vt = line.split(":")[-1].strip()
        if "Log" in line:
            result_log = line.split(":")[-1].strip()

    # 说话情绪
    emo = ""
    neu = 0
    ag = 0
    unk = 0
    for line in f_line:
        if "Neu" in line:
            neu += 1
        if "Ag" in line:
            ag += 1
        if "Unk" in line:
            unk += 1
    if neu != 0:
        emo += "Neu "
    if neu != 0:
        emo += "Ag "
    if neu != 0:
        emo += "Unk "

    # answer
    tim_rim = (re.findall("sult:[\s\S]*?Sum", f_read)[0][4:-3]).split("\n")
    del tim_rim[0]
    del tim_rim[-1]
    answer = ""
    for x in tim_rim:
        speak = x.split(":")[-1]
        a = re.sub("\[[\s\S]*?\]", "", speak)
        a = re.sub("[A-Za-z\d+]", "", a).strip()
        answer += a.decode("gbk", "ignore")

    pstt_result.write(
        "－－－－ >> case_id : " + case_id + "\n"
        + "\n 说明 : " + explain
        + "\n 测试类型 : pstt-asr-one"
        + "\n 测试时间 : " + str(run_time) + "秒"
        + "\n 音频文件 : " + wav_name
        + "\n 内存占用 : " + str(cpu)
        + "\n LogId : " + result_log
        + "\n LogId/16 : " + str(float(result_log) / 16)
        + "\n VoiceTime : " + result_vt
        + "\n Answer : " + answer
        + "\n ExceptAnswer : " + test_refs["answer"]
        + "\n Emo : " + emo
        + "\n ExceptEmo : Neu Ag Unk \n"
    )

    # 时间边界验证(单句)

    pstt_result.write(" 时间边界验证(单句)，错误结果如下 : ↓\n\n")

    for line in tim_rim:
        line = line.split(":")[-1]
        print line
        speak_time = re.findall("\([\s\S]*?\)", line)
        valid = "0"
        for i in speak_time:
            if int(valid) > int(i.split("/")[0].split("-")[-1]):
                pstt_result.write(line)
                break
            else:
                valid = i.split("/")[0].split("-")[-1]

    # 时间边界验证(上下句)-------------------------------------------------------------!!!!!!!!!!!!
    pstt_result.write(" 时间边界验证(上下句)，错误结果如下 : ↓\n\n")
    previous_line = ""
    valid = "0"
    for line in tim_rim:
        line = line.split(":")[-1]
        line_spk_time = re.findall("\[[\s\S]*?\]", line)
        try:
            line_valid_time = line_spk_time[0].split("-")[-1].split("/")[0]
        except Exception as e:
            print e
            break
        if int(valid) > int(line_valid_time):
            pstt_result.write("上句 ： " + previous_line)
            pstt_result.write("下句 ： " + line + "\n")
        previous_line = line
        valid = line_spk_time[-1].split("-")[-1][:-1].split("/")[0]

    # 执行对比
    if answer == test_refs["answer"] and emo != "":
        pstt_result.write(" 测试结果 : " + case_id + "第" + count + "轮测试成功\n\n")
    else:
        pstt_result.write(" 测试结果 : " + case_id + "第" + count + "轮测试失败\n\n")


def pstt_spkemone_report(case_id, count, explain, test_refs, pstt_result, cpu, regs, wav_name, speaker,
                         main_path, run_time):

    test_refs = eval(test_refs)
    result_vt = ""
    result_log = ""
    with open(main_path + "../client/result_one.txt", "r") as f:
        f_line = f.readlines()
    with open(main_path + "../client/result_one.txt", "r") as f:
        f_read = f.read()
    for line in f_line:
        if "Voice Time" in line:
            result_vt = line.split(":")[-1].strip()
        if "Log" in line:
            result_log = line.split(":")[-1].strip()

    # 说话情绪
    emo = ""
    neu = 0
    ag = 0
    unk = 0
    for line in f_line:
        if "Neu" in line:
            neu += 1
        if "Ag" in line:
            ag += 1
        if "Unk" in line:
            unk += 1
    if neu != 0:
        emo += "Neu "
    if neu != 0:
        emo += "Ag "
    if neu != 0:
        emo += "Unk "

    # 说话人验证
    if "A[" in f_read and "B[" not in f_read:
        speaker = "A"
    if "A[" not in f_read and "B[" in f_read:
        speaker = "B"
    if "A[" in f_read and "B[" in f_read:
        speaker = "A B"

    # answer
    tim_rim = (re.findall("sult:[\s\S]*?Sum", f_read)[0][4:-3]).split("\n")
    del tim_rim[0]
    del tim_rim[-1]
    answer = ""
    for x in tim_rim:
        speak = x.split(":")[-1]
        a = re.sub("\[[\s\S]*?\]", "", speak)
        a = re.sub("[A-Za-z\d+]", "", a).strip()
        answer += a.decode("gbk", "ignore")
    answer = re.sub("\([\s\S]*?\)", "", answer)
    pstt_result.write(
        "－－－－ >> case_id : " + case_id + "\n"
        + "\n 说明 : " + explain
        + "\n 测试类型 : pstt-asr-one"
        + "\n 测试时间 : " + str(run_time) + "秒"
        + "\n 音频文件 : " + wav_name
        + "\n 内存占用 : " + str(cpu)
        + "\n LogId : " + result_log
        + "\n LogId/16 : " + str(float(result_log) / 16)
        + "\n VoiceTime : " + result_vt
        + "\n Answer : " + answer
        + "\n ExceptAnswer : " + test_refs["answer"]
        + "\n Emo : " + emo
        + "\n ExceptEmo : Neu Ag Unk "
        + "\n Speaker : " + speaker
        + "\n ExceptSpeaker : A B \n"
    )

    # 时间边界验证(单句)

    pstt_result.write(" 时间边界验证(单句)，错误结果如下 : ↓\n\n")

    for line in tim_rim:
        line = line.split(":")[-1]
        print line
        speak_time = re.findall("\([\s\S]*?\)", line)
        valid = "0"
        for i in speak_time:
            if int(valid) > int(i.split("/")[0].split("-")[-1]):
                pstt_result.write(line)
                break
            else:
                valid = i.split("/")[0].split("-")[-1]

    # 时间边界验证(上下句)-------------------------------------------------------------!!!!!!!!!!!!
    pstt_result.write(" 时间边界验证(上下句)，错误结果如下 : ↓\n\n")
    previous_line = ""
    valid = "0"
    for line in tim_rim:
        line = line.split(":")[-1]
        line_spk_time = re.findall("\[[\s\S]*?\]", line)
        try:
            line_valid_time = line_spk_time[0].split("-")[-1].split("/")[0]
        except Exception as e:
            print e
            break
        if int(valid) > int(line_valid_time):
            pstt_result.write("上句 ： " + previous_line)
            pstt_result.write("下句 ： " + line + "\n")
        previous_line = line
        valid = line_spk_time[-1].split("-")[-1][:-1].split("/")[0]

    # 执行对比
    if answer == test_refs["answer"] and emo != "" and speaker == "A B":
        pstt_result.write(" 测试结果 : " + case_id + "第" + count + "轮测试成功\n\n")
    else:
        pstt_result.write(" 测试结果 : " + case_id + "第" + count + "轮测试失败\n\n")


def pstt_token_report(test_case, main_path, test_refs, pstt_result, explain, case_id):

    s_time = time.time()
    test_case = eval(test_case)
    print test_case["token_ip"]
    print test_case["token_cport"]
    print test_case["token_pm"]
    os.system(main_path + "pstt_token " + test_case["token_ip"] + " " + test_case["token_cport"] + " "
              + test_case["token_pm"] + " > " + main_path + "token.txt")
    with open(main_path + "token.txt", "r") as token_read:
        token_read_lines = token_read.readlines()
    token = token_read_lines[1].split(":")[1]
    e_time = time.time()
    run_time = str(round((float(e_time)-float(s_time)), 2))

    pstt_result.write(
        "－－－－ >> case_id : " + case_id + "\n"
        + "\n 说明 : " + explain
        + "\n 测试类型 : pstt-asr-one"
        + "\n 测试时间 : " + str(run_time) + "秒"
        + "\n Token : " + token
        + "\n ExceptToken : " + test_refs["token"]
    )


def pstt_pre_report(case_id, count, explain, test_refs, pstt_result, prt, drt, cpu, regs, wav_name, run_time, main_path):

    test_refs = eval(test_refs)
    pstt_result.write(
        "－－－－ >> case_id : " + case_id + "\n"
        + "\n 说明 : " + explain
        + "\n 测试类型 : pstt - asr - pre"
        + "\n 测试时间 : " + str(run_time) + "秒"
        + "\n 音频文件 : toolong"
        + "\n 执行速度 : { prt : " + prt + " drt : " + drt + " }"
        + "\n 期待执行速度 : { prt : " + test_refs["rt"]["prt"] + " brt : " + test_refs["rt"]["drt"] + " }"
        + "\n cpu和内存详细信息如下：↓↓"
    )
    with open(main_path + "pre.txt", "r") as f:
        f_line = f.readlines()
    for line in f_line:
        pstt_result.write(line)

    # rt对比
    if prt >= test_refs["rt"]["prt"] and drt >= test_refs["rt"]["drt"]:
        rt_valid = True
    else:
        rt_valid = False

    if rt_valid is True:
        pstt_result.write("测试结果 : " + case_id + "第" + count + "轮测试成功\n\n")
    else:
        pstt_result.write("测试结果 : " + case_id + "第" + count + "轮测试失败\n\n")

