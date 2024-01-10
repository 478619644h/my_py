import base64
import re
import os
import json
import time
import requests

pattern = re.compile(r'({.*?})', re.S)
domain = "http://172.16.33.240:8083"

def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    index = 0
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        print("处理文件:[%s]"%(child))
        current = 1
        with open(child, "r") as file:
            for row in file:
                print("%s 的第%d行"%(child,current))
                jsonStr = re.findall(pattern,row)[0]
                jsonObj = json.loads(jsonStr)

                reportTime = int(jsonObj["dateTime"])
                if reportTime > 1609300800000:
                    jsonObj["body"] = base64.b64decode(jsonObj["body"]).decode("utf-8")

                    timeArray = time.localtime(reportTime/1000)
                    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    print(jsonObj)
                    print(reportTime)
                    print(otherStyleTime)
                    r = requests.post(url='%s/garbagesortiot/kichen.do?getkichendata'%(domain),json=jsonObj)
                    if r.status_code != 200:
                        print("响应错误 程序退出")
                        return

                current = current+1



if __name__ == "__main__":
    eachFile("./iotchuyudata/")

