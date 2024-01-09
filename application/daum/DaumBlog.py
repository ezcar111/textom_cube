import os, sys, time, random
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
import urllib.request as urllib2
import http.cookiejar as cookielib
import re
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from earthling.service.Logging import log
from application.daum.DaumBase import DaumBase

class DaumBlog(DaumBase):
    # url_search        = "http://search.daum.net/search?w=blog&nil_search=btn&enc=utf8&q=%(query)s&m=board&%(date_query)s&p=%(start)d&SA=tistory"
    url_search        = "https://search.daum.net/search?w=fusion&col=blog&q=%(query)s&DA=STC&p=%(start)d&period=u&%(date_query)s&sort=recency"
    def search(self, 
        query, 
        idx_num, 
        stop, 
        num=1, 
        start=1, 
        pause=2.0, 
        date_start='', 
        date_end='',
        out_filepath=''):

        self.set_cookie_jar("blog")

        query1 =query
        query = urllib.parse.quote_plus(query)
        date_query = 'sd='+date_start.replace("-", "")+'000000&ed='+date_end.replace("-", "")+'235959'
        settings = self.get_settings("blog")
        stop = settings["max_count"]
        repeat_count = settings["repeat_count"]

        now = time.localtime()
        uniq_file_name = str(now.tm_year) +"_"+ str(now.tm_mon) +"_"+ str(now.tm_mday) +"_"+ str(now.tm_hour) +"_"+ str(now.tm_min) +"_"+ str(now.tm_sec)
        # out_file = open(file_name+"file_daum_data/"+uniq_file_name+"_daum_blog.txt","a")
        out_file = open(out_filepath,"a")

        count_web = 0
        html_status = 200

        while 1:
            url = self.url_search % vars()
            if start > repeat_count:
                break

            self.monit_url(url)
            html, html_status = self.get_page(url, True)
            if html_status != 200:
                return out_file.name, count_web, html_status
                
            time.sleep(3)
            soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")

            list_html = []
            try:
                list_html = soup('c-doc-web')
            except Exception as err:
                log.debug("데이터가 존재하지 않습니다.")

            for item in list_html:
                try:
                    title = re.sub(r'<(/)?c-title.*?>', '', str(item('c-title')[0])).strip()
                except:
                    title = ""

                try:
                    link = item('c-title')[0].get('data-href')
                except:
                    link = ""

                try:
                    text = re.sub(r'<(/)?c-contents-desc.*?>', '', str(item('c-contents-desc')[0])).strip().replace("\n", " ").replace("<b>", "").replace("</b>", "")
                except:
                    text = ""

                try:
                    if title != "" and link != "" and text != "":
                        scrape_text = title + '\t' + link +'\t'+ text
                        out_file.write(scrape_text + "\n")
                        count_web = count_web + 1

                        self.monit_count(
                            idx_num=idx_num, 
                            query=query1, 
                            current_item_count=count_web, 
                            scrape_text=scrape_text
                        )
                        
                except:
                    pass

            settings = self.get_settings("blog")
            if count_web > settings["max_count"]:
                break

            if len(list_html) < 9:
                break
            start = start + 1

            delay_time = settings["delay_time"]
            time.sleep(delay_time)

            self.monit_current(
                current_repeat_count=start, 
                max_repeat_count=repeat_count, 
                current_item_count=count_web, 
                max_item_count=1000, 
                delay_time=stop)
            # time.sleep(random.randrange(1, 11))

        try :
            out_file.close()
        except:
            pass

        return out_file.name, count_web, html_status