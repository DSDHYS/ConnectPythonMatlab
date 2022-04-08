# -*- coding: utf-8 -*-
"""
Created on Sat May  1 18:56:48 2021

@author: Xie
"""
import re
import os
import format_class
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.contrib.distributions import MultivariateNormalFullCovariance
from tensorflow.python.ops.parallel_for.gradients import jacobian
from collections import Iterable
import Communication as cmnc
import time
import traceback
import subprocess
import math


# message = target_address + ";" + self.source_address + ";" + str(code) + ";" + str(len(data)) + ";" + str(data) + ";" + str(round(sum(data),2)) + "\n"
# 数据通信中操作码规定:
# 请求数据                               77
# 发送心率数据                      95
# 发送发电量数据                  35
# 发送外骨骼数据theta       44
# 数据已接收                           57


class nes_alg:
    def __init__(self, dna_size=2, n_pop=6, n_generation=6, lr=0.3):
        self.DNA_SIZE = dna_size
        self.N_POP = n_pop
        self.N_GENERATION = n_generation
        self.LR = lr

    def flatten(self, items, ignore_types=(str, bytes)):
        for x in items:
            if isinstance(x, Iterable) and not isinstance(x, ignore_types):
                yield from self.flatten(x)
            else:
                yield x

    def get_fitness(self, pred):
        self.comm = cmnc.Communication("NC", "/dev/ttyTHS1")
        to_send = -((pred[:, 0])**2 + (pred[:, 1])**2)
        to_send = np.array(to_send)
        to_send = self.dataProcessing(to_send)
        print(to_send)
        # return to_send
        # to_send=[99900]

        dst = 'HR'

        while True:
            # asking for data from HR belt
            self.comm.com.reset_output_buffer()
            self.comm.send(dst, 0, to_send)
            # print(to_send)
            rec = self.comm.receive()

            self.comm.com.reset_input_buffer()
            if rec == 'HR':
                print("\n\nReceived:{}".format(rec))
                print("Calculation is ongoing...\n")
                break
            else:
                print("Waiting HR data!")
                self.comm.com.reset_output_buffer()
                self.comm.send(dst, 0, to_send)
                time.sleep(0.5)
        time.sleep(15)
        # print("properties:",comm.properties[rec])
        return self.comm.properties[rec]

    def dataProcessing(self, origin):
        mystr = str(origin)
        mystr = mystr.strip('[')
        mystr = mystr.strip(']')
        mystr = mystr.strip(' ')
        mystr = re.sub(' +', ' ', mystr).split(' ')
        output = []
        for mem in mystr:
            output.append(float(mem))
        return output

    def saveData(self, time, rtime, power, heartRate):
        df = pd.DataFrame(data=[[time, rtime, power, heartRate]], columns=[
                          'Time', 'relativeTime', 'Power', 'heartRate'])
        if os.path.exists("myData.csv"):
            fileData = pd.read_csv("myData.csv")
            df = fileData.append(df)
        df.to_csv("myData.csv", index=False)
        print("Data is saved successfully to myData.csv")

    def sleepWake(self, sleepTime):
        # 此处设置nano休眠时间
        subprocess.call(
            "sudo rtcwake -m mem -s {}".format(sleepTime), shell=True)

        # 唤醒后正常运作
        print("Nano is awake and ready to work!")

    def objFunc(self,Txe,Txs):
        Tx1=1
        Tx2=6
        t=np.arange(Txe,Txs,0.01)
        PGx= self.commPW.properties['PW']
        px=2*PGx/(math.cos(math.pi*(Tx1-Txs)/(Txe-Txs))-math.cos(math.pi*(Tx2-Txs)/(Txe-Txs)))
        
        trajectX=px*math.pi/(2*(Txe-Txs))*math.sin(math.pi/(Txe-Txs)*(t-Txs))
        
        return trajectX

    def getMsg(self, dst,commMsg):
        #self.commMsg = cmnc.Communication("NC", "COM7")
        to_send = []
        to_send = np.array(to_send)
        if to_send != []:
            to_send = self.dataProcessing(to_send)
        while True:
            # Requesting for data from HR belt
            commMsg.com.reset_output_buffer()
            commMsg.send(dst, commMsg.codeRequest, to_send)
            rec = ' '
            code = ' '
            # rec, code = self.commHR.receive()

            try:
                rec, code = commMsg.receive()
            except Exception as e:
                print("-------------Data cannot be unpacked!--------------")
                print(traceback.print_exc())
            commMsg.com.reset_input_buffer()

            if rec == dst and (code == str(commMsg.codeReceive)):
                # 确认接受到了信息
                print("\n\nReceived:{}".format(rec))
                print("Request has been tended.")
                # print("Data:{}".format(self.commMsg.properties[rec]))
                # 发送信息通知其无需继续发送数据
                # self.commMsg.send(dst, self.commMsg.codeReceive, to_send)
                # print("Calculation is ongoing...\n")
                break
            elif rec == dst and (code ==str(commMsg.codeSendHR)):
                # 确认接受到了信息
                print("\n\nReceived:{}".format(rec))
                print("Data:{}".format(commMsg.properties[rec]))
                # 发送信息通知其无需继续发送数据
                commMsg.send(dst, commMsg.codeReceive, to_send)
                # print("Calculation is ongoing...\n")
                break
            else:
                # 未接受信息 继续请求数据
                print("Waiting for {} data!".format(dst))
                commMsg.com.reset_output_buffer()
                commMsg.send(dst, commMsg.codeRequest, to_send)
                time.sleep(0.5)
        time.sleep(5)
        # print("properties:",self.comm.properties[rec])

        # 数据暂存入communication类中
        return commMsg.properties[rec]

    def getHR(self):
        # self.comm.send("LE",1,mean_value)
        # self.comm.send("RE",1,mean_value)
        self.commHR = cmnc.Communication("NC", "/dev/ttyTHS1")
        to_send = []
        to_send = np.array(to_send)
        if to_send != []:
            to_send = self.dataProcessing(to_send)
        # []
        dst = 'HR'
        while True:
            # Requesting for data from HR belt
            self.commHR.com.reset_output_buffer()
            self.commHR.send(dst, self.commHR.codeRequest, to_send)
            rec = ' '
            code = ' '
            # rec, code = self.commHR.receive()

            try:
                rec, code = self.commHR.receive()
            except Exception as e:
                print(traceback.print_exc())
            self.commHR.com.reset_input_buffer()

            if rec == 'HR' and (code == str(self.commHR.codeReceive) or str(self.commHR.codeSendHR)):
                # 确认接受到了信息
                print("\n\nReceived:{}".format(rec))
                print("Data:{}".format(self.commHR.properties[rec]))
                # 发送信息给 HR 通知其无需继续发送数据
                self.commHR.send(dst, self.commHR.codeReceive, to_send)
                # print("Calculation is ongoing...\n")
                break
            else:
                # 未接受信息 继续请求数据
                print("Waiting for HR data!")
                self.commHR.com.reset_output_buffer()
                self.commHR.send(dst, self.commHR.codeRequest, to_send)
                time.sleep(0.5)
        time.sleep(15)
        # print("properties:",self.comm.properties[rec])

        # 数据暂存入communication类中
        return self.commHR.properties[rec]

    def getPW(self):
        # self.comm.send("LE",1,mean_value)
        # self.comm.send("RE",1,mean_value)
        self.commPW = cmnc.Communication("NC", "/dev/ttyTHS1")
        to_send = []
        to_send = np.array(to_send)
        if to_send != []:
            to_send = self.dataProcessing(to_send)
        # print(to_send)
        # return to_send

        # []
        dst = 'PW'
        while True:
            # Requesting for data from PW belt
            self.commPW.com.reset_output_buffer()
            self.commPW.send(dst, self.commPW.codeRequest, to_send)
            rec = ' '
            code = ' '
            try:
                rec, code = self.commPW.receive()
            except:
                print("Data has been lost!")
            self.commPW.com.reset_input_buffer()

            if rec == 'PW' and (code == str(self.commPW.codeReceive)):
                # 确认接受到了信息
                print("\n\nReceived:{}".format(rec))
                # 发送信息给 PW 通知其无需继续发送数据
                self.commPW.send(dst, self.commPW.codeReceive, to_send)
                # print("Calculation is ongoing...\n")
                break
            else:
                # 未接受信息 继续请求数据
                print("Waiting for PW data!")
                self.commPW.com.reset_output_buffer()
                self.commPW.send(dst, self.commPW.codeRequest, to_send)
                time.sleep(0.5)
        time.sleep(15)
        # print("properties:",self.comm.properties[rec])

        # 数据暂存入communication类中
        return self.commPW.properties[rec]

    def getLE(self):
        # self.comm.send("LE",1,mean_value)
        # self.comm.send("RE",1,mean_value)
        self.commLE = cmnc.Communication("NC", "/dev/ttyTHS1")
        to_send = []
        to_send = np.array(to_send)
        if to_send != []:
            to_send = self.dataProcessing(to_send)
        # print(to_send)
        # return to_send

        # []
        dst = 'LE'
        while True:
            # Requesting for data from LE belt
            self.commLE.com.reset_output_buffer()
            self.commLE.send(dst, self.commLE.codeRequest, to_send)
            rec = ' '
            code = ' '
            try:
                rec, code = self.commLE.receive()
            except:
                print("Data has been lost!")
            self.commLE.com.reset_input_buffer()

            if rec == 'LE' and (code == str(self.commLE.codeReceive)):
                # 确认接受到了信息
                print("\n\nReceived:{}".format(rec))
                # 发送信息给 LE 通知其无需继续发送数据
                self.commLE.send(dst, self.commLE.codeReceive, to_send)
                # print("Calculation is ongoing...\n")
                break
            else:
                # 未接受信息 继续请求数据
                print("Waiting for LE data!")
                self.commLE.com.reset_output_buffer()
                self.commLE.send(dst, self.commLE.codeRequest, to_send)
                time.sleep(0.5)
        time.sleep(15)
        # print("properties:",self.comm.properties[rec])

        # 数据暂存入communication类中
        return self.commLE.properties[rec]

    def getRE(self):
        # self.comm.send("LE",1,mean_value)
        # self.comm.send("RE",1,mean_value)
        self.commRE = cmnc.Communication("NC", "/dev/ttyTHS1")
        to_send = []
        to_send = np.array(to_send)
        if to_send != []:
            to_send = self.dataProcessing(to_send)
        # print(to_send)
        # return to_send

        # []
        dst = 'RE'
        while True:
            # Requesting for data from RE belt
            self.commRE.com.reset_output_buffer()
            self.commRE.send(dst, self.commRE.codeRequest, to_send)
            rec = ' '
            code = ' '
            try:
                rec, code = self.commRE.receive()
            except:
                print("Data has been lost!")
            self.commRE.com.reset_input_buffer()

            if rec == 'RE' and (code == str(self.commRE.codeReceive)):
                # 确认接受到了信息
                print("\n\nReceived:{}".format(rec))
                # 发送信息给 RE 通知其无需继续发送数据
                self.commRE.send(dst, self.commRE.codeReceive, to_send)
                # print("Calculation is ongoing...\n")
                break
            else:
                # 未接受信息 继续请求数据
                print("Waiting for RE data!")
                self.commRE.com.reset_output_buffer()
                self.commRE.send(dst, self.commRE.codeRequest, to_send)
                time.sleep(0.5)
        time.sleep(15)
        # print("properties:",self.comm.properties[rec])

        # 数据暂存入communication类中
        return self.commRE.properties[rec]

    def giveLE(self, formattedData):
        # self.comm.send("LE",1,mean_value)
        # self.comm.send("RE",1,mean_value)
        self.commLE = cmnc.Communication("NC", "/dev/ttyTHS1")
        formattedData = np.array(formattedData)
        formattedData = self.dataProcessing(formattedData)
        emptyList = []
        emptyList = np.array(emptyList)
        if emptyList != []:
            emptyList = self.dataProcessing(emptyList)

        # []
        dst = 'LE'
        while True:
            # Send data to LE belt
            self.commLE.com.reset_output_buffer()
            self.commLE.send(dst, self.commLE.codeSendTheta, formattedData)
            rec = ' '
            code = ' '
            try:
                rec, code = self.commLE.receive()
            except:
                print("Data has been lost!")
            self.commLE.com.reset_input_buffer()

            if rec == 'LE' and (code == str(self.commLE.codeReceive)):
                # 确认接受到了确认的回复信息 无需继续发送
                print("\n\nReceived:{}".format(rec))
                break
            else:
                # 未接受回复 继续发送数据
                print("Waiting for LE responses!")
                self.commLE.com.reset_output_buffer()
                self.commLE.send(dst, self.commLE.codeSendTheta, emptyList)
                time.sleep(0.5)
        time.sleep(15)
        # print("properties:",self.comm.properties[rec])

        # 数据暂存入communication类中
        return self.commLE.properties[rec]

    def giveRE(self, formattedData):
        # self.comm.send("LE",1,mean_value)
        # self.comm.send("RE",1,mean_value)
        self.commRE = cmnc.Communication("NC", "/dev/ttyTHS1")
        formattedData = np.array(formattedData)
        formattedData = self.dataProcessing(formattedData)
        emptyList = []
        emptyList = np.array(emptyList)
        if emptyList != []:
            emptyList = self.dataProcessing(emptyList)
        # print(to_send)
        # return to_send

        # []
        dst = 'RE'
        while True:
            # Send data to RE belt
            self.commRE.com.reset_output_buffer()
            self.commRE.send(dst, self.commRE.codeSendTheta, formattedData)
            rec = ' '
            code = ' '
            try:
                rec, code = self.commRE.receive()
            except:
                print("Data has been lost!")
            self.commRE.com.reset_input_buffer()

            if rec == 'RE' and (code == str(self.commRE.codeReceive)):
                # 确认接受到了确认的回复信息 无需继续发送数据
                print("\n\nReceived:{}".format(rec))
                break
            else:
                # 未接受回复 继续发送数据
                print("Waiting for RE responses!")
                self.commRE.com.reset_output_buffer()
                self.commRE.send(dst, self.commRE.codeSendTheta, emptyList)
                time.sleep(0.5)
        time.sleep(15)
        # print("properties:",self.comm.properties[rec])

        # 数据暂存入communication类中
        return self.commRE.properties[rec]

    def givePW(self, formattedData):
        # self.comm.send("LE",1,mean_value)
        # self.comm.send("RE",1,mean_value)
        self.commPW = cmnc.Communication("NC", "/dev/ttyTHS1")
        formattedData = np.array(formattedData)
        formattedData = self.dataProcessing(formattedData)
        emptyList = []
        emptyList = np.array(emptyList)
        if emptyList != []:
            emptyList = self.dataProcessing(emptyList)
        # print(to_send)
        # return to_send

        # []
        dst = 'PW'
        while True:
            # Send data to RE belt
            self.commPW.com.reset_output_buffer()
            self.commPW.send(dst, self.commPW.codeSendTheta, formattedData)
            rec = ' '
            code = ' '
            try:
                rec, code = self.commHR.receive()
            except:
                print("Data has been lost!")
            self.commPW.com.reset_input_buffer()

            if rec == 'PW' and (code == str(self.commPW.codeReceive)):
                # 确认接受到了确认的回复信息 无需继续发送数据
                print("\n\nReceived:{}".format(rec))
                break
            else:
                # 未接受回复 继续发送数据
                print("Waiting for PW responses!")
                self.commPW.com.reset_output_buffer()
                self.commPW.send(dst, self.commPW.codeSendTheta, emptyList)
                time.sleep(0.5)
        time.sleep(10)
        # print("properties:",self.comm.properties[rec])

        # 数据暂存入communication类中
        return self.commPW.properties[rec]

    def giveMsg(self, formattedData, dst):
        # self.comm.send("LE",1,mean_value)
        # self.comm.send("RE",1,mean_value)
        self.commGMsg = cmnc.Communication("NC", "/dev/ttyTHS1")
        formattedData = np.array(formattedData)
        if formattedData != []:
            formattedData = self.dataProcessing(formattedData)
        emptyList = []
        emptyList = np.array(emptyList)


        # []
        while True:
            # Send data to LE belt
            self.commGMsg.com.reset_output_buffer()
            self.commGMsg.send(dst, self.commGMsg.codeSendTheta, formattedData)
            rec = ' '
            code = ' '
            try:
                rec, code = self.commGMsg.receive()
            except Exception as e:
                print(traceback.print_exc())
            self.commGMsg.com.reset_input_buffer()

            if rec == dst and (code == str(self.commGMsg.codeReceive)):
                # 确认接受到了确认的回复信息 无需继续发送
                print("\n\nReceived:{}".format(rec))
                break
            else:
                # 未接受回复 继续发送数据
                print("Waiting for LE responses!")
                self.commGMsg.com.reset_output_buffer()
                self.commGMsg.send(dst, self.commGMsg.codeSendTheta, emptyList)
                time.sleep(0.5)
        time.sleep(15)
        # print("properties:",self.comm.properties[rec])

        # 数据暂存入communication类中
        return self.commGMsg.properties[rec]

    def training(self, num, mu, myCov):
        # mean = tf.Variable(tf.random_normal([2, ], [5.,1.], 1.), dtype=tf.float32)
        # mean = tf.Variable(tf.constant(mu), dtype=tf.float32)
        # cov = tf.Variable(myCov * tf.eye(self.DNA_SIZE), dtype=tf.float32)
        # mvn = MultivariateNormalFullCovariance(loc=mean, covariance_matrix=cov)
        # make_kid = mvn.sample(self.N_POP)
        # mu 包含 Txe Txs 
        mean = tf.Variable(tf.constant(mu), dtype=tf.float32)
        cov = tf.Variable(myCov * tf.eye(self.DNA_SIZE), dtype=tf.float32)
        mvn = MultivariateNormalFullCovariance(loc=mean, covariance_matrix=cov)
        make_kid = mvn.sample(self.N_POP)

        tfkids_fit = tf.placeholder(tf.float32, [self.N_POP, ])
        tfkids = tf.placeholder(tf.float32, [self.N_POP, self.DNA_SIZE])

        mean_new = tf.placeholder(tf.float32, [2, ])
        cov_new = tf.placeholder(tf.float32, [2, 2])

        mean_update = tf.assign(mean, mean_new)
        cov_update = tf.assign(cov, cov_new)

        # mvn_logPro=mvn.log_prob(tfkids)
        fit_mvnLogPro = mvn.log_prob(tfkids)*tfkids_fit

        J_fitMvnLogPro = jacobian(fit_mvnLogPro, [mean, cov])
        # J_mvnLogPro=jacobian(mvn_logPro,[mean,cov])

        sess = tf.Session()
        # initialize tf variables
        sess.run(tf.global_variables_initializer())

        # training
        # while self.G < self.N_GENERATION:
        for g in range(self.N_GENERATION):
            kids = sess.run(make_kid)
            # 在主函数 发送make_kid 和 mean 给左右外骨骼
            toSend = [str(num), kids]
            self.giveLE(toSend)
            self.giveRE(toSend)

            # 绝对初始时间记录
            t_0 = time.time()

            # 请求HR 让心率带开始工作
            self.getHR()
            # 休眠12min
            self.sleepWake(5)

            # print("Time: ", time.ctime(time.time()))

            # getPW
            power = self.getPW()

            # getHR
            # kids_fit = self.get_fitness(kids)
            # 苏醒 请求发电量 请求12min采集到的心率
            kids_fit = self.getHR()

            # getTime
            t_1 = time.time()
            absTime = time.ctime(t_1)
            relativeTime = t_1-t_0

            # 保存数据 myData.csv
            self.saveData(absTime, relativeTime, power, kids_fit)

            J_M = sess.run(J_fitMvnLogPro, {
                           tfkids_fit: kids_fit, tfkids: kids})
            J_flat = list(self.flatten(J_M))
            J = np.array([0, 0, 0, 0, 0, 0])
            for i in range(self.N_POP):
                J_mat = np.array([J_flat[i*2+0], J_flat[i*2+1], J_flat[i*4+2*self.N_POP],
                                 J_flat[i*4+2*self.N_POP], J_flat[i*4+2*self.N_POP], J_flat[i*4+2*self.N_POP]])
                J = J[0]+J_mat[0], J[1]+J_mat[1], J[2]+J_mat[2], J[3] + \
                    J_mat[3], J[4]+J_mat[4], J[5]+J_mat[5]
            J_gra = np.reshape(np.array(J)/20, (6, 1))

            mean_o = np.array(sess.run(mean))
            cov_o = np.array(sess.run(cov))

            mean_value = (np.array(sess.run(mean)) +
                          self.LR*J_gra[0:2].flatten())
            cov_value = (np.array(sess.run(cov)) +
                         self.LR*J_gra[2:6].reshape(2, 2))
            print("x and y values: ", mean_value)

            '''
            #约束边界
            if mean_value[0]<0.5:
                mean_value[0]=0.5
            if mean_value[1]>0.7:
                mean_value[1]=0.7
            
            '''
            sess.run(mean_update, {mean_new: mean_value})
            sess.run(cov_update, {cov_new: cov_value})
            print("Parameters are successfully updated!")

            self.sleepWake(2)
            self.G = self.G + 1

            try:
                sess.run(make_kid)
                runMean = sess.run(mean_update)
                toSend = [str(num), runMean]
                self.giveLE(toSend)
                self.giveRE(toSend)

            except:
                print("Parameters are wrongly updated!")
                sess.run(mean_update, {mean_new: mean_o})
                sess.run(cov_update, {cov_new: cov_o})


# 确认外骨骼接收到了信息后 心率带等待请求 nano请求心率带数据  确认心率带收到后nano 心率带睡眠1min  nano 休眠12min 心率带开始采集12min(2min 中拿1min HR)
# 心率带采集完 nano苏醒 nano发送getHR请求 心率带收到请求发送数据 确认nano收到后等待新的请求
# nano迭代一次 发送theta给左右外骨骼 确认外骨骼接收到数据后进入休眠状态 12min
# 发电量在getHR前获取并保存


    