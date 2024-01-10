# /usr/bin/python
# -*- coding: utf-8 -*-
#author: hyj
#date: 2019/11/14

import re
import requests
import random

def spiderPic(html,keyword):
    print("正在查找：" + keyword + "对应的图片")
    for addr in re.findall('"objURL":"(.*?)"',html,re.S):
        print('正在爬取的url为 '+str(addr))
        r = requests.get(addr,stream=True,verify=False,timeout=10)
        if r.status_code == 200:
            with open(r'./images/'+str(random.randint(1,1000))+".jpg", 'wb+') as f:
                for chunk in r.iter_content(chunk_size=1024):  # 循环写入，chunk_size是文件大小
                    f.write(chunk)


def chpSpider():
    for i in range(1,100):
        r = requests.get("https://zuanbot.com/api.php?level=min&lang=zh_cn")
        print(r.text)


if __name__ == '__main__':
    chpSpider()
    # word = input("请输入您想要抓取的图像关键词")
    # searchUrl = "https://image.baidu.com/search/index?tn=baiduimage&ie=utf-8&word=" + word
    # result = requests.get(searchUrl)
    # print(result.text)
    #spiderPic(result.text,word)
    # pattern = re.compile(r'\d+')  # 查找数字
    # result1 = pattern.findall('runoob 123 google 456')
    # result2 = pattern.findall('run88oob123google456', 0, 10)
    # print(result1)
    # print(result2)