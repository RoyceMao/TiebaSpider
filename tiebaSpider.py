# -*- coding:utf-8 -*-

from bs4 import *
import os
import urllib.parse
import urllib.request
from lxml import etree


def loadImage(link):
    """
    作用：爬取每个帖子里面出现的所有图片
    :param link: 帖子链接
    """
    global count
    endpage = 1
    # 创建文件夹
    path = os.getcwd()
    new_path = os.path.join(path, "Pic_load")
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    # 计算出每个帖子的翻页数量
    myurl = urllib.request.urlopen(link).read().decode('utf-8')
    soup = BeautifulSoup(myurl)
    list = soup.find_all('span', attrs={'class': 'red'})
    i = 1
    if list:
        for li in list:
            if len(li.attrs) > 1:
                continue
            else:
                endpage = int(li.string)
                break
    # 根据html标签下载每个帖子下的所有图片
    while i <= endpage:
        # print link + '?pn=' + str(i)
        mypage = urllib.request.urlopen(link + '?pn=' + str(i)).read().decode('utf-8')
        # print u'打开网页成功'
        soup = BeautifulSoup(mypage)
        listimg = soup.find_all('img', attrs={'class': 'BDE_Image'})
        for li in listimg:
            src = li['src']
            print(u'开始下载第 %d 幅图片' % count)
            # print src
            # noinspection PyBroadException
            try:
                content = urllib.request.urlopen(src).read()
                f = open(os.path.join(new_path, '%d.jpg') % count, 'wb')
                # print content
                f.write(content)
            except:
                print(u'出现异常 下载下一张')
                continue
            f.close()
            print(u'完成！')
            count += 1
        i += 1
    print(u'--------该帖子下图片下载全部完成--------')


def loadPage(url_page):
    """
    作用：根据url发送请求，获取服务器的响应文件，并组合出每个帖子的链接
    :param url_page: 需要爬取的url地址
    """
    request = urllib.request.Request(url_page)
    html = urllib.request.urlopen(request).read()
    # 解析HTML文档为HTML DOM模型
    content = etree.HTML(html)
    # print content
    # 返回所有匹配成功的当页每个帖子链接的列表集合
    link_list = content.xpath(u'//li/div[@class="t_con cleafix"]/div/div/div/a/@href')
    print("共 %d 个帖子" % len(link_list))
    # print(link_list)
    for link in link_list:
        if link_list.index(link) > 0: # 跳过一般性吧规贴
            fulllink = "http://tieba.baidu.com" + link
            # 组合为每个帖子的链接
            print("--------进入该页面第 %d 个帖子--------" % (link_list.index(link) + 1))
            loadImage(fulllink)


def tiebaSpider(link, beginPage, endPage):
    """
    作用：贴吧爬虫调度器，负责组合处理每个页面的url
    :param link : 贴吧首页url的前部分
    :param beginPage : 起始页page
    :param endPage : 结束页page
    """
    for page in range(beginPage, endPage + 1):
        pn = (page - 1) * 50
        fulllink = link + "&pn=" + str(pn)
        print("========开始加载 Page (%d) ========" % page)
        # print fullurl
        loadPage(fulllink)
        # print html
        print("========Page (%d) 的图片爬取完毕========" % page)


if __name__ == "__main__":
    count = 1
    kw = input("请输入需要爬取的贴吧名:")
    startPage = int(input("请输入起始页："))
    stopPage = int(input("请输入结束页："))

    url = "http://tieba.baidu.com/f?"
    key = urllib.parse.urlencode({"kw": kw})
    fullurl = url + key
    print(fullurl)
    tiebaSpider(fullurl, startPage, stopPage)
