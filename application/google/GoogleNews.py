from bs4 import BeautifulSoup
import os

import time
import urllib
import urllib.request as urllib2
from earthling.service.Logging import log
from earthling.handler.earthling_dao import exec
from application.google.GoogleBase import GoogleBase


class GoogleNews(GoogleBase):
    # URL templates to make Google searches.
    # url_search = "https://www.google.co.kr/search?hl=ko&num=100&q=%(query)s&tbm=nws&btnG=Google+Search&start=%(start)d&%(date_query)s&lr=lang_ko"
    url_search = "https://www.google.co.kr/search?hl=ko&num=100&q=%(query)s&tbm=nws&btnG=Google+Search&start=%(start)d&%(date_query)s"

    def search(
        self,
        query,
        idx_num,
        stop = 1000,
        tld='co.kr', 
        lang='ko', 
        num=100, 
        start=0, 
        pause=2.0, 
        date_start='', 
        date_end='',
        out_filepath=''):

        settings = self.get_settings("news")
        stop = settings["max_count"]
        link_list = []
        query1 =query
        query = urllib.parse.quote_plus(query)
        date_query = 'tbs=cdr%3A1%2Ccd_min%3A'+date_start+'.%2Ccd_max%3A'+date_end+'.&filter=0'
        out_file = open(out_filepath, "a")

        count_web = 0
        page_web = 0
        start = 0
        html_status = 200
        #stop = 1000

        while start < stop:
            if page_web > 10:
                break
            # Sleep between requests.
            time.sleep(pause)

            # Request the Google Search results page.
            url = self.url_search % vars()
            html, html_status = self.get_page(url)
            if html_status != 200:
                break


            soup = BeautifulSoup(html,"html.parser",from_encoding="utf-8")
            list_html = []
            try:
                #list_html = soup('a', {'class' : 'WlydOe'})
                list_html = soup('div', {'class' : 'SoaBEf'})
            except Exception as err:
                log.debug("데이터가 존재하지 않습니다.")

            if list_html == []:
                break

            for item in list_html:
                try:
                    #link = item.get('href')
                    link = item('a')[0].get("href").strip()
                except:
                    link = ""

                try:
                    #title = item('div', {'class' : 'mCBkyc'})[0].text.strip()
                    title = item.find(attrs = {'role' : 'heading'}).text.strip()
                except:
                    title = ""

                try:
                    #text = item('div', {'class' : 'GI74Re'})[0].text.strip().replace("\n", " ")
                    text = item('div', {'class' : 'GI74Re nDgy9d'})[0].text.strip()
                except:
                    text = ""

                try:
                    #if title != "" and link != "" and text != "":
                    # time.sleep(1)
                    scrape_text = title + '\t' + link +'\t'+ text
                    out_file.write(scrape_text + '\n')
                    count_web = count_web + 1
                    log.debug(f"task-[{idx_num}] 수집 중 => 키워드: {query1}, 카운트: {count_web}, 내용: {scrape_text[0:30]}")
                except Exception as err:
                    log.debug(err)
                    continue

            start = start + 100
            if start > 1000:
                break

            if len(list_html) < 90:
                break

            settings = self.get_settings("facebook")
            delay_time = settings["delay_time"]
            log.debug(f"Trying... {start} / 100.. Wait {delay_time} seconds")
            time.sleep(delay_time)
            
        try :
            out_file.close()
        except:
            pass

        return out_file.name, count_web, html_status
    
# if __name__ == "__main__":
    # google_web_search("Vpp player", "719347", stop=1000, date_start='2022-03-20', date_end='2021-04-20')