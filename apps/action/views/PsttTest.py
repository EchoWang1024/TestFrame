# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.testservice.views import report_manager
from socket import *
import os
import time
import re
import random
import threading


class PsttTest(object):

    def __init__(self, message, test_case, test_id, data, test_tools,
                 explain, test_refs, scene, test_folder, count, case_id, test_result):

        self.message = message
        self.test_case = test_case
        self.test_id = test_id
        self.data = data
        self.test_tools = test_tools
        self.explain = explain
        self.test_refs = test_refs
        self.scene = scene
        self.test_folder = test_folder
        self.count = count
        self.case_id = case_id
        self.test_result = test_result
        self.pstt_main = self.test_folder + "/pstt/pstt_client-4.1.0/"
        self.pstt_sum = self.test_folder + "/pstt/pstt_calc_recrate/"
        self.conf_valid = ""
        self.run_cpu = ""
        self.prt = ""
        self.brt = ""
        self.rate = ""
        self.wav_name = ""
        self.speaker = ""
        self.run_time = ""
        self.emo_valid = ""
        self.spk_der = ""
        self.test_port = ""
        self.test_cport = ""
        self.rt_port = ""
        self.pre_valid = 0
        self.pstt_port_dis()
        self.pstt_main_test()

    '''main'''

    def pstt_port_dis(self):

        # 分配port
        project_path = os.path.dirname(__file__)
        pstt_port_file = os.path.join(project_path, "../../../pstt-port.txt")
        with open(pstt_port_file, "r") as f:
            f_line = f.readlines()
        ports = []
        for line in f_line:
            if line == "\n":
                continue
            ports.append(line.strip())
        port = random.sample(ports, 1)
        self.test_port = port[0]
        ports.remove(port[0])
        with open(pstt_port_file, "w") as w:
            for i in ports:
                w.write(i.strip() + "\n")
        # 分配cport
        if port[0] == "7788":
            self.test_cport = "5452"
            self.rt_port = "5453"
        if port[0] == "7789":
            self.test_cport = "5462"
            self.rt_port = "5463"
        if port[0] == "7790":
            self.test_cport = "5472"
            self.rt_port = "5473"

    def pstt_main_test(self):

        print self.case_id + " pstt " + self.scene + " 测试开始... "

        if self.scene == "asr":

            # 执行步骤
            self.server_restart()
            self.test_valid()
            for i in self.conf_valid:
                self.client_conf_change(i)
                self.client_start()
                self.pstt_cpu()
                self.client_tag_result(i)
                self.client_asr_merge()
                self.client_rt()
                self.client_rate()

                # 生成报告
                report_manager.pstt_asr_report(self.case_id, self.count, self.explain, self.test_refs, self.test_result,
                                               self.prt, self.brt, self.run_cpu, self.rate, self.wav_name, self.run_time)

        if self.scene == "spk":

            # 执行步骤
            self.server_restart()
            self.test_valid()
            for i in self.conf_valid:
                self.client_conf_change(i)
                self.client_start()
                self.pstt_cpu()
                self.client_tag_result(i)
                self.client_spk_merge()
                self.client_spk_der()
                self.client_rt()
                self.client_rate()
                self.client_spk_speaker()

                # 生成报告
                report_manager.pstt_spk_report(self.case_id, self.count, self.explain, self.test_refs, self.test_result,
                                               self.prt, self.brt, self.run_cpu, self.rate, self.wav_name, self.speaker,
                                               self.pstt_main, self.run_time, self.spk_der)

                # 客户端配置初始化
                os.system("rm -rf " + self.pstt_main + "../spk_tools")
                os.system("cp -rf /part/home/pachiratest/pstt/spk_tools " + self.pstt_main + "../")

        if self.scene == "spkem":

            # 执行步骤
            self.server_restart()
            self.test_valid()
            # 测试验证
            for i in self.conf_valid:
                self.client_conf_change(i)
                self.client_start()
                self.pstt_cpu()
                self.client_tag_result(i)
                self.client_spk_merge()
                self.client_rt()
                self.client_rate()
                self.client_spk_speaker()
                self.client_emo_valid()

                # 生成报告
                report_manager.pstt_spkem_report(self.case_id, self.count, self.explain, self.test_refs, self.test_result,
                                                 self.prt, self.brt, self.run_cpu, self.rate, self.wav_name, self.speaker,
                                                 self.pstt_main, self.run_time, self.emo_valid)

        if self.scene == "token":

            report_manager.pstt_token_report(self.test_case, self.pstt_main, self.test_refs, self.test_result,
                                             self.explain, self.case_id)

        if self.scene == "asr_one":

            self.server_restart()
            self.pstt_one_start()
            self.pstt_cpu()

            report_manager.pstt_asrone_report(self.case_id, self.count, self.explain, self.test_refs, self.test_result,
                                              self.run_cpu, self.rate, self.wav_name, self.speaker, self.pstt_main,
                                              self.run_time)

        if self.scene == "spk_one":

            self.server_restart()
            self.pstt_one_start()
            self.pstt_cpu()

            report_manager.pstt_spkone_report(self.case_id, self.count, self.explain, self.test_refs, self.test_result,
                                              self.run_cpu, self.rate, self.wav_name, self.speaker, self.pstt_main,
                                              self.run_time)

        if self.scene == "emo_one":

            self.server_restart()
            self.pstt_one_start()
            self.pstt_cpu()

            report_manager.pstt_emoone_report(self.case_id, self.count, self.explain, self.test_refs, self.test_result,
                                              self.run_cpu, self.rate, self.wav_name, self.speaker, self.pstt_main,
                                              self.run_time)

        if self.scene == "spkem_one":

            self.server_restart()
            self.pstt_one_start()
            self.pstt_cpu()

            report_manager.pstt_spkemone_report(self.case_id, self.count, self.explain, self.test_refs, self.test_result,
                                                self.run_cpu, self.rate, self.wav_name, self.speaker, self.pstt_main,
                                                self.run_time)

        if "pre" in self.scene:

            self.server_restart()
            self.test_valid()
            for i in self.conf_valid:
                self.client_conf_change(i)
                # 开启线程
                t1 = threading.Thread(target=self.client_start, args="")
                t2 = threading.Thread(target=self.server_pre, args="")
                t1.start()
                t2.start()
                t1.join()
                t2.join()
                self.client_rt()

                # 测试报告
                report_manager.pstt_pre_report(self.case_id, self.count, self.explain, self.test_refs, self.test_result,
                                               self.prt, self.brt, self.run_cpu, self.rate, self.wav_name,
                                               self.run_time, self.pstt_main)

                # 客户端配置初始化
                os.system("rm -rf " + self.pstt_main + "../spk_tools")
                os.system("cp -rf /part/home/pachiratest/pstt/spk_tools " + self.pstt_main + "../")

        self.pstt_reset()

    ''' public '''

    def server_restart(self):

        print("服务端准备重启")
        tcp_client = socket(AF_INET, SOCK_STREAM)
        ser_ads = ("192.168.128.61", int(self.test_port))
        tcp_client.connect(ser_ads)
        tcp_client.send(self.test_case)
        tcp_client.close()
        time.sleep(20)

    def test_valid(self):

        # 匹配所有的pstt_client_conf
        client_conf = re.findall("pstt_client.conf[0-9]", self.test_case)
        if len(client_conf) == 0:
            client_conf = ["pstt_client.conf"]
        self.conf_valid = client_conf

    def client_conf_change(self, conf_name):

        test_case = eval(self.test_case)[conf_name]

        # 判断是否计算token
        if "token" in eval(self.test_case).keys():
            os.system(self.pstt_main + "pstt_token 192.168.128.61 " + self.rt_port + " token > " + self.pstt_main
                      + "token.txt")
            with open(self.pstt_main + "token.txt", "r") as token_read:
                token_read_lines = token_read.readlines()
            token = token_read_lines[1].split(":")[1]
            test_case.setdefault("TOKEN", token.strip())

        # 配置客户端conf
        pstt_key = []
        for key in test_case:
            pstt_key.append(key)
        pstt_key.append("REC_RES_FILE")
        f_read = open(self.pstt_main + "pstt_client.conf", "r")
        f_rel = f_read.readlines()
        f_read.close()
        f_write = open(self.pstt_main + "pstt_client.conf", "w")
        for line in f_rel:
            valid = 0
            for key in pstt_key:
                if key in line:
                    valid += 1
            if valid == 0:
                f_write.write(line)
        for key in test_case:
            f_write.write(key + " = \"" + test_case[key] + "\";\n")

        # 报告所在位置
        pstt_result = self.pstt_main + "pstt_result.txt"
        f_write.write("REC_RES_FILE = " + "\"" + pstt_result + "\";\n")
        f_write.write("SERVER_PORT = " + "\"" + self.test_cport + "\";\n")
        f_write.close()

    def client_start(self):

        # 执行
        print "pstt_main正在执行中。。。"
        s_time = time.time()
        print(self.pstt_main + "pstt_client-4.1.0" + " -f " + self.pstt_main + "pstt_client.conf")
        os.system(self.pstt_main + "pstt_client-4.1.0" + " -f " + self.pstt_main + "pstt_client.conf")
        e_time = time.time()
        run_time = round(float(e_time-s_time), 2)
        self.run_time = run_time
        self.pre_valid = 1

    def client_tag_result(self, conf_name):

        # 标注文件 >> 标准结果 >> 格式转换
        test_case = eval(self.test_case)[conf_name]
        file_list = test_case["AUDIO_LIST_FILE"]
        f = open(file_list, "r")
        f_list = []
        os.system("mkdir " + self.pstt_main + "voice_list")
        for i in f.readlines():
            f_list.append(i.strip())
            os.system("cp " + i.strip() + " " + self.pstt_main + "voice_list/")
            print("cp " + i.strip() + " " + self.pstt_main + "voice_list/")
            i_grid = str(i[:-5]) + ".TextGrid"
            os.system("cp " + i_grid + " " + self.pstt_main + "voice_list/")
        print "java -jar " + self.pstt_main + "MergeGridResult.jar " + self.pstt_main + "voice_list/"
        os.system("java -jar " + self.pstt_main + "MergeGridResult.jar " + self.pstt_main + "voice_list/")
        result_true = open(self.pstt_main + "voice_list/audioConfig.txt", "r")
        result_list = []
        for line in result_true.readlines():
            result_list.append(line.split("=")[1])
        result_true.close()
        result_second = open(self.pstt_main + "voice_list/audioConfig.txt", "w")
        for x, y in zip(f_list, result_list):
            result_second.write(x + "\t" + y.strip() + "\n")
        result_second.close()
        os.system("iconv -f utf-8 -ct gbk " + self.pstt_main + "voice_list/audioConfig.txt > "
                  + self.pstt_main + "audioConfig.txt")
        # 音频文件名称获取
        wav_list = ""
        for i in f_list:
            wav_list += (str(i.split("/")[-1]) + "; ")
        self.wav_name = wav_list

    def client_rate(self):
        
        # 计算识别率
        os.system("python " + self.pstt_sum + "pasr_calc_recrate.py -s " + self.pstt_sum + "sclite -m "
                  + self.pstt_main + "audioConfig.txt -r " + self.pstt_main
                  + "pstt_result_merge.txt -o " + self.pstt_main + "test.rate -t array")
        with open(self.pstt_main + "test.rate", "r") as rate:
            self.rate = rate.readlines()[:5]

    def client_rt(self):
        
        # 计算速度
        os.system(self.pstt_main + "pstt_token 192.168.128.61 " + self.rt_port + " rt > " + self.pstt_main + "rt.txt")
        with open(self.pstt_main + "rt.txt", "r") as rt_file:
            rt_f_read = rt_file.read()
        prt = (rt_f_read.split(" ")[-1].strip()).split(":")[1]
        brt = rt_f_read.split(" ")[-2].split(":")[1]
        self.prt = prt
        self.brt = brt

    def pstt_one_start(self):

        # 执行pstt-one
        s_time = time.time()
        os.system(self.pstt_main + "../client/pstt_client"
                                 + " -i " + eval(self.test_case)["i"]
                                 + " -f " + eval(self.test_case)["f"]
                                 + " -t " + eval(self.test_case)["t"]
                                 + " -r " + eval(self.test_case)["r"]
                                 + " -b " + eval(self.test_case)["b"]
                                 + " -p " + self.test_cport
                                 + " -s " + eval(self.test_case)["s"]
                                 + " > " + self.pstt_main + "../client/result_one.txt"
                  )
        e_time = time.time()
        self.run_time = round(float(e_time)-float(s_time))
        self.wav_name = eval(self.test_case)["f"].split("/")[-1]

    def pstt_reset(self):

        # 服务端配置初始化
        tcp_client = socket(AF_INET, SOCK_STREAM)
        ser_ads = ('192.168.128.61', int(self.test_port))
        tcp_client.connect(ser_ads)
        tcp_client.send("reset_conf")
        tcp_client.close()
        self.test_result.close()
        # 还原使用后的端口
        project_path = os.path.dirname(__file__)
        pstt_port_file = os.path.join(project_path, "../../../pstt-port.txt")
        with open(pstt_port_file, "a") as f:
            f.write(self.test_port + "\n")

    def pstt_cpu(self):

        print "pstt获取cpu"
        tcp_client = socket(AF_INET, SOCK_STREAM)
        ser_ads = ("192.168.128.61", int(self.test_port))
        tcp_client.connect(ser_ads)
        tcp_client.send("pstt_cpu")
        memory = tcp_client.recv(1024)
        self.run_cpu = memory + "g"
        tcp_client.close()

    ''' asr '''

    def client_asr_merge(self):

        # 合并结果
        os.system("java -jar " + self.pstt_main + "MergeLongRecs.jar "
                  + self.pstt_main + "pstt_result.txt pstt_result_merge.txt")

    ''' spk '''

    def client_spk_merge(self):

        os.system("cp -rf " + self.pstt_main + "voice_list/* " + self.pstt_main + "../spk_tools/data/wav")
        os.system("java -jar " + self.pstt_main + "MergeLongRecs_SPK.jar "
                  + self.pstt_main + "pstt_result.txt pstt_result_merge.txt")

    def client_spk_der(self):

        if "config.cfg.example" in eval(self.test_case).keys():
            # spk 计算der步骤要放在操作标准文件之后（因为voice_list还是空的）
            tcp_client = socket(AF_INET, SOCK_STREAM)
            ser_ads = ('192.168.128.61', self.test_port)
            tcp_client.connect(ser_ads)
            tcp_client.send("get_spk_seg")
            print("pstt-spk 等待返回seg压缩包...")
            with open(self.pstt_main + "../spk_tools/data/seg/sd_result.zip", "ab") as f:
                while True:
                    rec_dat = tcp_client.recv(1024)
                    if not rec_dat:
                        break
                    f.write(rec_dat)
            tcp_client.close()
            os.system("unzip " + self.pstt_main + "../spk_tools/data/seg/sd_result.zip -d "
                      + self.pstt_main + "../spk_tools/data/seg/")
            os.system(self.pstt_main + "../spk_tools/spk_run.sh -i " + self.pstt_main + "../spk_tools/data/ -o "
                      + self.pstt_main + "../spk_tools/result")
        else:
            self.spk_der = "1"

    def client_spk_speaker(self):

        # 对存在的说话人进行判断
        speaker_a = 0
        speaker_b = 0
        with open(self.pstt_main + "pstt_result.txt", "r") as f:
            for line in f.readlines():
                if "A" in str(line.decode("gbk")):
                    speaker_a += 1
                if "B" in str(line.decode("gbk")):
                    speaker_b += 1

        if speaker_a != 0 and speaker_b != 0:
            self.speaker = "A,B"
        if speaker_a == 0 and speaker_b != 0:
            self.speaker = "B"
        if speaker_a != 0 and speaker_b == 0:
            self.speaker = "A"

    ''' emo '''
    def client_emo_valid(self):

        # 对存在的情绪进行判断
        neu = 0
        ag = 0
        unk = 0
        with open(self.pstt_main + "pstt_result.txt", "r") as f:
            for line in f.readlines():
                if "Neu" in line.decode("gbk", "ignore"):
                    neu += 1
                if "Ag" in str(line.decode("gbk", "ignore")):
                    ag += 1
                if "Unk" in str(line.decode("gbk", "ignore")):
                    unk += 1
        if neu != 0:
            self.emo_valid += "Neu "
        if ag != 0:
            self.emo_valid += "Ag "
        if unk != 0:
            self.emo_valid += "Unk "
        if neu == 0 and ag == 0 and unk == 0:
            self.emo_valid = "None"

    ''' pre '''
    def server_pre(self):

        # 在执行前判断是否进行压力测试
        print("服务端开始监控cpu和内存变化,每１０分钟获取一次参数")

        while True:
            if self.pre_valid == 1:
                break
            tcp_client = socket(AF_INET, SOCK_STREAM)
            ser_ads = ("192.168.128.61", int(self.test_port))
            tcp_client.connect(ser_ads)
            tcp_client.send("pretest")
            data = tcp_client.recv(1024)
            print data
            data = eval(data)
            now_time = data[0]
            cpu = data[1]
            mem_s = data[2]
            print "pre 写入"
            with open(self.pstt_main + "pre.txt", "a") as f:
                f.write("time : " + now_time + " cpu : " + cpu + " memory : " + mem_s + "g\n")
            tcp_client.close()
            time.sleep(600)


