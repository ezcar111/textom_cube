from bs4 import BeautifulSoup
import os
import time
import urllib
import urllib.request as urllib2
# import urllib2

from earthling.service.Logging import log
# import application.settings as settings
from earthling.handler.earthling_dao import exec
from application.googlecn.GoogleCnBase import GoogleCnBase

"""
url_home          = "https://www.google.%(tld)s/"
url_search        = "https://www.google.%(tld)s/search?hl=%(lang)s&num=100&q=%(query1)s&btnG=Google+Search&%(date_query)s"
url_next_page     = "https://www.google.%(tld)s/search?hl=%(lang)s&num=100&q=%(query1)s&start=%(start)d&%(date_query)s"
url_search_num    = "https://www.google.%(tld)s/search?hl=%(lang)s&num=100&q=%(query1)s&btnG=Google+Search&%(date_query)s"
url_next_page_num = "https://www.google.%(tld)s/search?hl=%(lang)s&num=100&q=%(query1)s&start=%(start)d&%(date_query)s"
"""
# zh-CN
class GoogleCnAcademic(GoogleCnBase):
    # url_search = "https://www.google.co.kr/search?hl=ko&q=%(query1)s&btnG=Google+Search&start=%(start)d&%(date_query)s&lr=lang_ko"
    url_search = "https://www.google.%(tld)s/search?hl=%(lang)s&num=100&q=%(query)s&btnG=Google+Search&%(date_query)s"
    def get_url(self, query, page=1, start_date='', end_date=''):
        query = urllib.parse.quote_plus(query)
        
        # query = urllib.quote_plus(query)
        if start_date != '' and end_date != '':
            start_year = start_date.split("-")[0]
            end_year = end_date.split("-")[0]
        
            url = "https://scholar.google.com.hk/scholar?q=" + query + "&start=" + str(page) + "&hl=zh-CN&as_sdt=0%2C5&as_ylo=" + start_year + "&as_yhi=" + end_year
        else:
            url = "https://scholar.google.com.hk/scholar?hl=zh-CN&as_sdt=0%2C5&q=" + query + "&btnG=&start=" + str(page)
        return url


    def search(
        self,
        query,
        idx_num,
        stop = 1000,
        tld='com', 
        lang='zh-CN', 
        num=100, 
        start=0, 
        pause=5.0, 
        date_start='', 
        date_end='',
        out_filepath=''):

        settings = self.get_settings("academic")
        stop = settings["max_count"]
        total_count = stop
        crawl_count = 0
        start, repeat_count = 0, settings["repeat_count"]
        out_file = open(out_filepath, 'a')

        date_start = date_start.replace(".+","-")
        date_end = date_end.replace(".+","-")
        date_start = date_start.split("-")[1] + "%2F" + date_start.split("-")[2] + "%2F" + date_start.split("-")[0]
        date_end = date_end.split("-")[1] + "%2F" + date_end.split("-")[2] + "%2F" + date_end.split("-")[0]
        
        html_status = 200    
        while_break = False
        while True:
            url = self.get_url(query, page=start, start_date=date_start, end_date=date_end)
            html, html_status = self.get_page(url)
            if html_status != 200:
                return out_file.name, crawl_count, html_status

            time.sleep(5)
            soup = BeautifulSoup(html, "html.parser")
            list_html = []
            try:
                item_area = soup("div", {"id" : "gs_res_ccl_mid"})[0]
                html_list = item_area("div", {"class" : "gs_r gs_or gs_scl"})
            except Exception as err:
                log.debug(err)

            if list_html == []:
                break
                
            for item in html_list:
                try:
                    title = item("h3", {"class" : "gs_rt"})[0].text
                except Exception as err:
                    log.debug(err)
                    title = ""
                
                try:
                    text = item("div", {"class" : "gs_rs"})[0].text
                except Exception as err:
                    log.debug(err)
                    text = ""
                
                try:
                    link = item("a")[0].get("href")
                except Exception as err:
                    log.debug(err)
                    link = ""

                try:
                    scrape_text = title + '\t' + link +'\t'+ text
                    out_file.write(scrape_text + '\n')
                    crawl_count = crawl_count + 1

                    self.monit_count(
                        idx_num=idx_num, 
                        query=query, 
                        current_item_count=crawl_count, 
                        scrape_text=scrape_text
                    )
                    
                    if crawl_count >= stop:
                        while_break = True
                        break

                except Exception as err:
                    log.debug(err)
                    continue

            if while_break == True:
                break
            
            settings = self.get_settings("academic")
            delay_time = settings["delay_time"]
            repeat_count = settings["repeat_count"]

            start = start + 1
            if start > repeat_count:
                break
            
            time.sleep(delay_time)
            self.monit_current(
                current_repeat_count=start, 
                max_repeat_count=repeat_count, 
                current_item_count=crawl_count, 
                max_item_count=stop, 
                delay_time=delay_time
            )

        try :
            out_file.close()
        except:
            pass

        return out_file.name, crawl_count, html_status


    
if __name__ == "__main__":
    google_web_search("Vpp player", "719347", stop=1000, date_start='2022-03-20', date_end='2021-04-20')
