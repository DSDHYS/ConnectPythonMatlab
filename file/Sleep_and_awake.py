# 利用python语句使nano进入休眠状态
import subprocess

# 此处设置休眠时间为20s
subprocess.call("sudo rtcwake -m mem -s 20",shell=True)

# 唤醒后正常运作
print("I am awake and ready to work!")
