import json
import re



def logRead(path="./log.txt"):
    with open(path, "r") as file:
        for line in file.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            #print(line)

            result = re.findall(".*[(.*)].*", line)
            for x in result:
                str = '['+x+']'
                logWriter(str+'\n')


def logWriter(line,path="./log-a.txt"):
    with open(path,'a+') as file:
        file.write(line)

def handle():
    with open("./log-b.txt") as f:
        count = 0
        for line in f.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            if findStrInFile("./log-a.txt",line):
                count = count+1
        print(count)

def findStrInFile(file, expStr):
    with open(file) as f:
        for line in f:

            if expStr in line:
                return True
    return False


logRead()
#handle()