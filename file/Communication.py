import serial
import time
import subprocess
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'


# message的操作码规则: str(code): 0-请求数据 1-发送第一段负功区间数据 2-发送第二段负功区间数据
# message = target_address + ";" + self.source_address + ";" + str(code) + ";" + str(len(data)) + ";" + str(data) + ";" + str(round(sum(data),2)) + "\n"
# message中的部分由分号分隔 目标地址+源地址+操作码+字符串长度+数据字符串+余数检验值
# 数据通信中操作码规定:
# 请求数据                               77
# 发送心率数据                      95
# 发送发电量数据                  35
# 发送外骨骼数据theta       44
# 数据已接收                           57


logic_data_start = 99900
logic_data_end = 99090


class Communication:

    # port is a device name: depending on operating system.
    # e.g. /dev/ttyTHS1 on GNU/Linux or COM3 on Windows.
    def __init__(self, source_address: str, port: str):
        # 数据通信中操作码规定:
        #  请求数据和确认接受到数据时  只发送空数组
        self.codeRequest = 77
        self.codeSendHR = 95
        self.codeSendPow = 35
        self.codeReceive = 57
        self.codeSendTheta = 44

        self.source_address = source_address
        # 打开端口
        subprocess.call("sudo chmod 777 " + port, shell=True)
        self.com = serial.Serial(port, 9600, timeout=0.5)
        if self.com.isOpen():
            print("Open port successfully")
        else:
            subprocess.call("sudo chmod 777 " + port, shell=True)
        # 初始化各属性值为负数
        self.properties = {"HR": -1.0, "LE": -1.0, "RE": -1.0}

    # 余数校验
    def check_remainder(self, num: list, remainder: float) -> bool:
        return (round(sum(num), 2)) == remainder

    def send(self, target_address: str, code: int, data: list):
        if type(data) == type(1):
            data = [data]
        message = target_address + ";" + self.source_address + ";" + \
            str(code) + ";" + str(len(data)) + ";" + \
            str(data) + ";" + str(round(sum(data), 2)) + "\r"+"\n"
        # 发送,以ASCII编码
        self.com.reset_output_buffer()
        print("message encoding:{}".format(message.encode(encoding='ASCII')))
        self.com.write(message.encode(encoding='ASCII'))

    # 并没有用处，其功能可以通过receive实现
    def message_get(self) -> int:
        pass

    def receive(self) -> str:
        raw = self.com.readline()
        # if raw==b'\xff':
        #    print("WRONG!")
        #    return "NONE"
        print("--------------------------------------------")##
        print("{}{}".format(raw, type(raw)))
        print("--------------------------------------------")##

        message = ""
        if raw:
            try:
                message = raw.decode(encoding='ASCII')
            except:
                return "NONE", 0
        if message == "":
            return "NONE", 0
        # 以分号分割
        words = message.split(';')
        print("**********************************")##
        print(words)
        print("**********************************")##

        # 解包
        dst, src, code, data_len, data, remainder = words
        data_len = int(data_len)
        data = data.split(",")
        data_temp = [x for x in range(data_len)]#定义数组大小
        for i in range(data_len):
            if i == 0:
                data_temp[i] = float(data[i][1:len(data[i])])
            elif i == data_len-1:
                data_temp[i] = float(data[i][0:len(data[i])-1])
            else:
                data_temp[i] = float(data[i])
        data = data_temp
        # 取整，以便后续余数校验
        remainder = float(remainder)
        if not self.check_remainder(data, remainder):
            print("余数校验失败")
            return "BAD", 0
        self.properties[src] = data
        print("New Message From {} Received. Data : {}".format(src, data))
        return src, code

# if __name__=="__main__":
    # # 对于发送端（Nano），则使用下面的代码
    # comm = Communication("NC", "/dev/ttyTHS1")
    # to_send = 34.56
    # dst = 'HR'
    # while True:
    #     comm.send(dst, 1, 99900)
    #     rec = comm.receive()
    #     if rec == dst:
    #         break

    # comm = Communication("HR", "COM4")

    # to_send = [34.56,23.6]
    # dst = 'NC'
    # comm.com.reset_output_buffer()
    # while True:
    # test.training()
    #     rec = comm.receive()
    #     comm.com.reset_output_buffer()
    #     print("Received: {}".format(rec))
    #     print(comm.properties)
    #     if rec == dst:
    #         comm.send(dst, 1, to_send)
    #     time.sleep(3)Receive:HR

        # 对于发送端（Nano），则使用下面的代码
    # comm = Communication("NC", "/dev/ttyTHS1")
    # to_send = [34.56,23.89]
    # dst = 'HR'
    # while True:
    #     comm.send(dst, 1,to_send)
    #     rec = comm.receive()
    #     if rec == dst:
    #         break
