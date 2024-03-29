from bs4 import BeautifulSoup
import os
import time
import urllib
import urllib.request as urllib2
# import urllib2

from earthling.service.Logging import log
# import application.settings as settings
from earthling.handler.earthling_dao import exec
from application.google.GoogleBase import GoogleBase

"""
url_home          = "https://www.google.%(tld)s/"
url_search        = "https://www.google.%(tld)s/search?hl=%(lang)s&num=100&q=%(query1)s&btnG=Google+Search&%(date_query)s"
url_next_page     = "https://www.google.%(tld)s/search?hl=%(lang)s&num=100&q=%(query1)s&start=%(start)d&%(date_query)s"
url_search_num    = "https://www.google.%(tld)s/search?hl=%(lang)s&num=100&q=%(query1)s&btnG=Google+Search&%(date_query)s"
url_next_page_num = "https://www.google.%(tld)s/search?hl=%(lang)s&num=100&q=%(query1)s&start=%(start)d&%(date_query)s"
"""

class GoogleWeb(GoogleBase):
    url_search = "https://www.google.co.kr/search?hl=ko&q=%(query1)s&btnG=Google+Search&start=%(start)d&%(date_query)s&lr=lang_ko"
    
    def search(
        self,
        query,
        idx_num,
        stop = 1000,
        tld='co.kr', 
        lang='ko', 
        num=100, 
        start=0, 
        pause=5.0, 
        date_start='', 
        date_end='',
        out_filepath=''):

        settings = self.get_settings("web")
        stop = settings["max_count"]
        total_count = stop
        crawl_count = 0
        start = 0
        out_file = open(out_filepath, 'a')

        date_start = date_start.replace(".+","-")
        date_end = date_end.replace(".+","-")
        date_start = date_start.split("-")[1] + "%2F" + date_start.split("-")[2] + "%2F" + date_start.split("-")[0]
        date_end = date_end.split("-")[1] + "%2F" + date_end.split("-")[2] + "%2F" + date_end.split("-")[0]
        
        date_query = 'tbs=cdr%3A1%2Ccd_min%3A'+date_start+'%2Ccd_max%3A'+date_end
        query1 = urllib.parse.quote_plus(query)
        html_status = 200
        # query1 = urllib.quote_plus(query)
        
        while_break = False
        while True:
            url = self.url_search % vars()
            html, html_status = self.get_page(url)
            if html_status != 200:
                break

            time.sleep(2)
            soup_list = BeautifulSoup(html, "html.parser")
            # list_html = soup_list('div', {'class' : 'g'})
            list_html = []
            try:
                list_html = soup_list('div', {'class' : 'g'})
            except Exception as err:
                log.debug(err)
            
            if list_html == []:
                break

            for item in list_html:
                if crawl_count >= total_count:
                    while_break = True
                    break

                try:
                    link = item('a')[0].get('href')
                    if link[-3:] == "pdf" or "download" in link:
                        continue
                except:
                    link = ""

                try:
                    title = item('h3')[0].text.strip()
                except:
                    title = ""

                try:
                    text = item('div', {'class' : 'VwiC3b'})[0].text
                except:
                    text = ""
                try:
                    scrape_text = title + '\t' + link +'\t'+ text
                    out_file.write(scrape_text + '\n')
                    crawl_count = crawl_count + 1
                    log.debug(f"task-[{idx_num}] 수집 중 => 키워드: {query}, 카운트: {crawl_count}, 내용: {scrape_text[0:30]}")
                except Exception as err:
                    log.debug(err)
                    continue

            if while_break == True:
                break

            if crawl_count > stop:
                break

            start = start + 10            
            if start > 100:
                break

            settings = self.get_settings("web")
            delay_time = settings["delay_time"]
            log.debug(f"Trying... {start} / {stop/10}.. Wait {delay_time} seconds")
            time.sleep(delay_time)

        try :
            out_file.close()
        except:
            pass

        return out_file.name, crawl_count, html_status


    
if __name__ == "__main__":
    google_web_search("Vpp player", "719347", stop=1000, date_start='2022-03-20', date_end='2021-04-20')
