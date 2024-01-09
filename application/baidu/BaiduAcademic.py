import re, time
from bs4 import BeautifulSoup
from .BaiduBase import BaiduBase
from datetime import datetime
from earthling.service.Logging import log
import urllib
import urllib.request as urllib2

class BaiduAcademic(BaiduBase):

    def __init__(self):
        super().__init__(data_type="academic")

    def get_url(self, keyword, page_count, start='', end=''):
        keyword = urllib.parse.quote_plus(keyword)
        if start != "" and end != "":
            url ='http://xueshu.baidu.com/s?wd='+keyword+'&pn='+str(page_count)+'&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&filter=sc_year%3D%7B'+str(start).strip().split("-")[0]+'%2C'+str(end).strip().split("-")[0]+'%7D&sc_hit=1'
        else:
            url = 'https://xueshu.baidu.com/s?wd=' + keyword + '&tn=SE_baiduxueshu_c1gjeupa&sc_hit=1&bcp=2&ie=utf-8&pn=' + str(page_count)
        return url


    def get_html_list(self, soup):
        html_list = []
        try:
            html_list = soup('div', {'class' : 'result sc_default_result xpath-log'})
        except Exception as err:
            log.debug(err)
        return html_list


    def get_resource(self, item):
        try:
            title = item('h3', {'class' : 't'})[0].text
        except:
            title = ""
        title = title.replace("\n", "").replace("\t", " ").strip()

        try:
            link = "https:" + item('a')[0].get('href')
        except:
            link = ""

        try:
            body_html = item('div', {'class' : 'c_abstract'})[0]
            body = body_html.get_text().strip()
        except:
            body = ""
        return title, link, body
