import re, time
from bs4 import BeautifulSoup
from .BaiduBase import BaiduBase
from datetime import datetime
from earthling.service.Logging import log
import urllib
import urllib.request as urllib2

class BaiduNews(BaiduBase):

    def __init__(self):
        super().__init__(data_type="news")

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
        url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=' + keyword + '&medium=0&pn=' + str(page_count) + '&gpc=stf%3D'+str(start_date)+'%2C'+str(end_date)+'%7Cstftype%3D2'
        return url


    def get_html_list(self, soup):
        html_list = []
        try:
            tmp = soup("div", {"id" : "content_left"})[0]
            html_list = tmp("div", {"class" : "new-pmd"})
        except Exception as err:
            log.debug(err)
        return html_list


    def get_resource(self, item):
        try:
            title = item("h3")[0].text.strip()
        except:
            title = ""
        title = title.replace("\n", "").replace("\t", " ").strip()

        try:
            link = item('a')[0].get('href')
        except:
            link = ""

        try:
            p = re.compile(" {2,}")
            body = item('span', {'class' : 'c-font-normal c-color-text'})[0].text
            body = body.strip().replace("\n", " ")
            body = p.sub(" ", body)
        except Exception as err:
            log.debug(err)
            body = ""
            
        log.debug(f"body: {body}")
        return title, link, body
