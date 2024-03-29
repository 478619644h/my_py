# -*-coding=utf-8-*-
import os
import re
import time
from urllib.parse import urljoin
from selenium import weakref
import requests
from bs4 import BeautifulSoup
from url_decode import urldecode


class GovSpider:

    def __init__(self):

        self.site_url = 'http://www.jiangxi.gov.cn/kzw/jxszfxxgkml/zfjg/zfld_12550/'

        self.spath = re.sub('.*//', '', self.site_url)

        sindex = self.spath.find('/')

        if sindex != -1:
            self.spath = self.spath[:sindex]

        self.base_path = '~/Desktop/gov_spider/'+self.spath
        print('base:',self.base_path)
    def start_page(self):

        req = webbrowser.Chrome()
        req.get(self.site_url)
        time.sleep(3)
        html1 = req.page_source
        soup = BeautifulSoup(html1,'lxml')
        iframes = soup.findAll('iframe')

        self.gs_runner(urldecode(html1))

        if iframes:
            print('有隐藏页面:',iframes)
            for ifr_url in iframes:

                if 'https:' not in ifr_url or 'http' not in ifr_url:
                    ifr_url = urljoin(self.site_url,ifr_url.get('src'))
                    print('进入隐藏页面：',ifr_url,'，并开启隐藏页面抓取img、css、js的程序........')
                try:
                    html2 = requests.get(ifr_url).text

                    self.gs_runner(urldecode(html2))
                except Exception as e:
                    print('隐藏页面的地址格式不正确,无法访问：',ifr_url)


        #程序运行完毕，自动关闭浏览器
        req.quit()


    def download_imgs(self,html):

        # 多筛选 防止无格式或不在src下的图片漏下
        liResult = re.findall('(".*?")',html)

        if liResult:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>正在下载img文件>>>>>>>>>>>>>>>>>>>>>>>>>')
            for img_li in liResult:
                        if img_li and ('{' not in img_li and '</' not in img_li) and('.jpg' in img_li or '.ico' in img_li or '.png' in
                           img_li or '.svg' in img_li or '.gif' in img_li or '.webp' in img_li or 'data:image' in img_li):

                            if '\/' not in img_li:
                                img_urls = [re.sub('[";]|(.*=)|(.*\()|(\).*)|(&quot)','',img_li)]
                            else:
                                img_urls = [re.sub('[";]','',img_li).replace('\/\/','//').replace('\/','//')]

                            if ',' in img_urls[0]:
                                print('检测到有js代码中有多路径img_url，正在深入抓取......')
                                img_urls = img_urls[0].split(',')
                            for img_url in img_urls:

                                try:
                                    if 'http:' not in img_url or 'https:' not in img_url:

                                        img_url = urljoin(self.site_url,img_url)

                                    img_name = re.sub('(.*//)', '', img_url)

                                    f_index = img_name.find('/')

                                    l_index = img_name.rfind('/')
                                    dir_path = self.spath+img_name[f_index:l_index]

                                    if not os.path.exists(dir_path):

                                        os.system('mkdir -p %s'%dir_path)

                                    img_name = re.sub('(.*/)', '', img_url)
                                    print('正在下载img文件：',img_url)
                                    img = requests.get(img_url).content

                                    with open('./%s' % (dir_path + '/' + img_name), 'wb') as f:
                                        f.write(img)
                                except Exception as e:
                                    print(img_url,e,'\r\nthis is uvaild url')

            print('===========================img文件下载完毕=============================')

    def download_js(self,html):

        liResult = re.findall('(".*?")',html)

        if liResult:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>正在下载js文件>>>>>>>>>>>>>>>>>>>>>>>>>')
            for on_url in liResult:
                if (on_url.endswith('.js"') or 'js?' in on_url) and 'src=' not in on_url:

                        js_links = [re.sub('(")|(.*:)', '', on_url)]

                        if ',' in js_links[0]:
                            print('检测到js代码中有多路径js_link，正在深入抓取.......')
                            js_links += js_links[0].split(',')

                        for js_link in js_links:
                            if 'http:' not in js_link or 'https:' not in js_link:

                                js_link = urljoin(self.site_url, js_link)

                            js_name = re.sub('(.*//)', '', js_link)
                            f_index = js_name.find('/')
                            l_index = js_name.rfind('/')
                            dir_path = self.spath+js_name[f_index:l_index]

                            if '/$' in dir_path:
                                dir_path = re.sub('(/\$)','/',dir_path)
                            if not os.path.exists(dir_path):

                                    os.system('mkdir -p %s'%dir_path)

                            print('正在下载js文件：',js_link)
                            js_file = requests.get(js_link).content
                            js_name = re.sub('(.*/)', '', js_link)

                            if js_name[0] == '$':
                                js_name = js_name.replace('$','')

                            with open('./%s'%dir_path+'/'+js_name,'wb') as f:

                                    f.write(js_file)

            print('===========================js文件下载完毕===========================')

    def download_css(self,html):


        liResult = re.findall('(".*?")',html)

        if liResult:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>正在下载css文件>>>>>>>>>>>>>>>>>>>>>>>>>')
            for on_url in liResult:

                if on_url.endswith('.css"') or 'css?' in on_url:

                    css_link = re.sub('["]','',on_url)

                    if 'http:' not in css_link or 'https:' not in css_link:
                        css_link = urljoin(self.site_url,css_link)

                    if css_link:
                        css_name = re.sub('(.*//)', '', css_link)
                        f_index = css_name.find('/')
                        l_index = css_name.rfind('/')
                        dir_path = self.spath+css_name[f_index:l_index]

                        if '/$' in dir_path:
                            dir_path = re.sub('(/\$)','/',dir_path)

                        if not os.path.exists(dir_path):

                            os.system('mkdir -p %s'%dir_path)

                        css_name = re.sub('(.*/)', '', css_link)
                        if css_name[0] == '$':
                            css_name = css_name.replace('$','')
                        print('正在下载css文件：',css_link)
                        css_file = requests.get(css_link).content

                        with open('./%s'%(dir_path+'/'+css_name) ,'wb') as f:

                            f.write(css_file)

            print('===========================css文件下载完毕===========================')

    def download_html(self,html):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>正在下载网页源码>>>>>>>>>>>>>>>>>>>>>>>>>')
        if not os.path.exists(self.spath+'/htmls'):
            print(self.base_path+'/htmls', '已经将html文件存在对应目录')
            os.system('mkdir -p %s' % self.spath+'/htmls')

        else:

            print(self.base_path+'/htmls', '已经存在此htmls目录')

        if html:

            with open('./%s' % (self.spath+'/htmls/'+self.spath+'.html'), 'w', encoding='utf-8') as f:

                    f.write(html)

        print('===========================下载网页源码完毕===========================')

    def gs_runner(self,html):

        self.download_html(html)
        self.download_imgs(html)
        self.download_css(html)
        self.download_js(html)
    def tip_sounds(self):
        pygame

if __name__ == '__main__':

    gs = GovSpider()
    gs.start_page()
