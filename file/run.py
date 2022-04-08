import time
import Communication as cmnc

import nes_class
import serial
# 1发送一号负功区间采样信息 + 二号负功区间均值信息
# 2发送二号负功区间采样信息 + 一号负功区间均值信息
# 0 表示请求信息，即等待接收信息

mu1 = [5.0, 3.0]
mu2 = [3.0, 2.0]
cov1 = 1.0
cov2 = 3.0
test1 = nes_class.nes_alg()
test2 = nes_class.nes_alg()
commMsg = cmnc.Communication("NC", "COM7")

# test1.getHR()
while True:
    msg = test1.getMsg('HR',commMsg)
    # if msg == []:
    #    test1.sleepWake(12)
    #print(msg)

    print("true")
        
    # com = serial.Serial("COM7", 9600, timeout=0.5)
    # com.close()

    # print(test1.getHR())
