import re, time
from bs4 import BeautifulSoup
from .BaiduBase import BaiduBase
from datetime import datetime
from earthling.service.Logging import log
import urllib
import urllib.request as urllib2

class BaiduWeb(BaiduBase):

    def __init__(self):
        super().__init__(data_type="web")


    def get_url(self, keyword, page_count, start='', end=''):

        keyword = urllib.parse.quote_plus(keyword)
        if start != "" and end != "":
            start = start + " 00:00:01"
            end = end + " 23:59:59"

            dt = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
            start_date = str(time.mktime(dt.timetuple())).split(".")[0]
            dt = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
            end_date =str(time.mktime(dt.timetuple())).split(".")[0]
        else:
            start_date = ""
            end_date = ""

        date_day ="rsv_enter=1&gpc=stf%3D"+str(start_date)+"%2C"+str(end_date)+"%7Cstftype%3D2&tfflag=1"
        url = "http://www.baidu.com/s?wd=" + keyword + "&pn=" + str(page_count) + "&" + str(date_day)
        return url
    
    def get_html_list(self, soup):
        html_list = []
        try:
            html_list = soup("div", {"class" : "result"})
        except Exception as err:
            log.debug(err)
        return html_list


    def get_resource(self, item):
        try:
            title = item('h3', {'class' : 't'})[0].text
        except Exception as err:
            log.debug(err)
            title = ""
        title = title.replace("\n", "").replace("\t", " ").strip()

        try:
            link = item('a')[0].get('href')
        except Exception as err:
            log.debug(err)
            link = ""

        try:
            body = item('span', {'class' : 'content-right_8Zs40'})[0].text.strip()
        except Exception as err:
            log.debug(err)
            body = ""

        return title, link, body
