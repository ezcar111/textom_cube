import os, sys, time, random
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
import urllib.request as urllib2
import http.cookiejar as cookielib

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from earthling.service.Logging import log
from application.daum.DaumBase import DaumBase

class DaumNews(DaumBase):
    url_search        = "https://search.daum.net/search?w=news&DA=PDG&q=%(query)s&%(date_query)s&p=%(start)d&spacing=0"

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

        self.set_cookie_jar("news")

        link_list =[]
        query1 =query

        query = urllib.parse.quote_plus(query)
        date_query = 'sd='+date_start.replace('-', '')+'000000&ed='+date_end.replace('-', '')+'235959'
        settings = self.get_settings("news")
        stop = settings["max_count"]

        now = time.localtime()
        uniq_file_name = str(now.tm_year) +"_"+ str(now.tm_mon) +"_"+ str(now.tm_mday) +"_"+ str(now.tm_hour) +"_"+ str(now.tm_min) +"_"+ str(now.tm_sec)
        # out_file = open(file_name+"file_daum_data/"+uniq_file_name+"_daum_news.txt","a")
        out_file = open(out_filepath,"a")

        chk =''
        count_web = 0
        html_status = 200

        while 1:
            url = self.url_search % vars()
            if start > 100:
                break

            html, html_status = self.get_page(url, False)
            if html_status != 200:
                return out_file.name, count_web, html_status

            time.sleep(3)
            soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
            
            try:
                # list_html = soup('div', {'class' : 'wrap_cont'})
                list_html = soup('div', {'class' : 'c-item-content'})
            except Exception as err:
                log.debug("데이터가 존재하지 않습니다.")

            for item in list_html:
                try:
                    # title = item('div', {'class' : 'item-title'})
                    title = item.find('div', {'class': 'item-title'})
                    title = title.find('a').text.strip()
                except:
                    title = ""

                try:
                    # link = item('a')[0].get('href')
                    link = item.find('div', {'class': 'item-title'})
                    link = link.find('a').get('href')
                except:
                    link = ""

                try:
                    # text = item('p', {'class' : 'desc'})[0].text.strip().replace("\n", " ")
                    text = item.find('div', {'class': 'item-contents'}).find('a').text.strip().replace("\n", " ")
                except:
                    text = ""

                try:
                    if title != "" and link != "" and text != "":
                        scrape_text = title + '\t' + link +'\t'+ text
                        out_file.write(scrape_text + "\n")
                        count_web = count_web + 1
                        log.debug(f"task-[{idx_num}] 수집 중 => 키워드: {query1}, 카운트: {count_web}, 내용: {scrape_text[0:30]}")
                except:
                    pass

            settings = self.get_settings("news")
            if count_web > settings["max_count"]:
                break

            if len(list_html) < 9:
                break
            start = start + 1
            delay_time = settings["delay_time"]
            time.sleep(delay_time)
            # time.sleep(random.randrange(1, 11))

        try :
            out_file.close()
        except:
            pass
        
        return out_file.name, count_web, html_status