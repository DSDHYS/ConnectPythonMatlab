# 使用示例:
""" 
# import format_class

# myFormat=format_class.formatter()

# print(myFormat.formatToSend(test1,mu1,cov1,test2,mu2,cov2))

"""


class formatter:
    def __init__(self):
        self.toSendDataset = []

    # 获取数据
    def collectData(self, myTest, num, mu, cov):
        myDataset = []
        myTest.saveFirstParam(num, mu, cov)
        for g in range(myTest.N_GENERATION):
            myData = myTest.training(num, mu, cov)
            if (myData is None) and (len(myDataset) > 0):
                myDataset.append(myDataset[g-1])
            elif (myData is None) and (len(myDataset) == 0):
                continue
            else:
                myDataset.append(myData)
        return myDataset

    # 将数组处理成所需要的形式
    def handleTwoMessages(self, set1, set2):
        self.toSendDataset = []
        smallerLen = 0
        if not (len(set1) == len(set2)):
            smallerLen = len(set1) if len(set1) < len(set2) else len(set2)
        else:
            smallerLen = len(set1)
        for i in range(smallerLen):
            item1, item2 = set1[i], set2[i]
            if (item1[0] == '1') and (item2[0] == '2'):
                self.toSendDataset.append([str(1), item1[1], item2[2]])
                self.toSendDataset.append([str(2), item2[1], item1[2]])
            elif (item1[0] == '2') and (item2[0] == '1'):
                self.toSendDataset.append([str(1), item2[1], item1[2]])
                self.toSendDataset.append([str(2), item1[1], item2[2]])
        return self.toSendDataset

    def formatToSend(self, test1, mu1, cov1, test2, mu2, cov2, num1=1, num2=2):
        # num是用于表明负功区间号数的标记
        testSet1 = self.collectData(test1, num1, mu1, cov2)
        testSet2 = self.collectData(test2, num2, mu2, cov2)
        return self.handleTwoMessages(testSet1, testSet2)
