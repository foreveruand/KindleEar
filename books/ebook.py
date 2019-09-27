#!/usr/bin/env python
# -*- coding:utf-8 -*-

from base import BaseFeedBook # 继承基类BaseFeedBook
from lib.urlopener import URLOpener
from bs4 import BeautifulSoup
# 返回此脚本定义的类名
def getBook():
    return ebook

# 继承基类BaseFeedBook
class ebook(BaseFeedBook):
    # 设定生成电子书的元数据
    title = u'笔趣阁' # 设定标题
    # __author__ = u'China Daily' # 设定作者
    description = u'第一序列、超神机械师、人皇纪' # 设定简介
    language = 'zh-cn' # 设定语言

    #coverfile = ''#设置封面
    #mastheadfile = ''#设定标头图片
    # 指定要提取的包含文章列表的主题页面链接
    # 每个主题是包含主题名和主题页面链接的元组
    feeds = [
        (u'第一序列', 'https://www.biquge5200.cc/117_117581/'),
        (u'超神机械师', 'https://www.biquge5200.cc/76_76215/'),
        (u'人皇纪', 'https://www.biquge5200.cc/44_44186/'),
    ]

    page_encoding = 'gbk'
    fulltext_by_readability = False

    keep_only_tags = [
        dict(name='div', class_='bookname'),
        dict(name='div', id='content'),
    ]

    # 提取每个主题页面下所有文章URL
    def ParseFeedUrls(self):
        urls = [] # 定义一个空的列表用来存放文章元组
        # 循环处理fees中两个主题页面
        for feed in self.feeds:
            # 分别获取元组中主题的名称和链接
            topic, url = feed[0], feed[1]
            # 请求主题链接并获取相应内容
            opener = URLOpener(self.host, timeout=self.timeout)
            result = opener.open(url)
            # 如果请求成功，并且页面内容不为空
            if result.status_code == 200 and result.content:
                # 将页面内容转换成BeatifulSoup对象
                soup = BeautifulSoup(result.content, 'lxml')
                # 找出当前页面文章列表中所有文章条目
                items = soup.find_all(name='div', id='list')
                # 循环处理每个文章条目
                for item in items:
                    title = item.a.string # 获取文章标题
                    link = item.a.get('href') # 获取文章链接
                    link = BaseFeedBook.urljoin(url, link) # 合成文章链接
                    urls.append((topic, title, link, None)) # 把文章元组加入列表
            # 如果请求失败通知到日志输出中
            else:
                self.log.warn('Fetch article failed(%s):%s' % \
                    (URLOpener.CodeMap(result.status_code), url))
        # 返回提取到的所有文章列表
        return urls