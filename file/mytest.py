import pandas as pd
import time

t_0 = time.time()
power = 35
hr = [32, 25, 67, 89, 94, 65]
t_1 = time.time()
absTime = time.ctime(t_1)
relativeTime = t_1-t_0
df = pd.DataFrame(data=[[absTime, relativeTime, power, hr]], columns=[
                  'Time', 'relativeTime', 'Power', 'heartRate'])
print(df)
