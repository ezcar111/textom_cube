from bs4 import BeautifulSoup
import http.cookiejar as cookielib
import os
import time
import urllib
import urllib.request as urllib2
#import urllib2

import datetime
from dateutil.relativedelta import relativedelta

import os, sys, re 
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from earthling.service.Logging import log
#import application.settings as settings
from earthling.handler.earthling_dao import exec
from application.naver.NaverBase import NaverBase


class NaverAcademic(NaverBase):

    # URL templates to make Naver searches.
    url_home          = "http://academic.naver.com/"
    url_search        = "http://academic.naver.com/search.naver?query=%(query)s&searchType=1&field=0&docType="
    url_next_page     = "http://academic.naver.com/search.naver?query=%(query)s&page=%(start)d&searchType=1&field=0&docType="
    url_search_num    = "http://academic.naver.com/search.naver?query=%(query)s&page=%(start)d&searchType=1&field=0&docType="
    url_next_page_num = "http://academic.naver.com/search.naver?query=%(query)s&page=%(start)d&searchType=1&field=0&docType="

    def get_search_url(self, query, date_start, date_end, num, start=0, is_next=False):
        # Prepare the URL of the first request.

        if is_next:
            url = self.url_next_page % vars() if num == 1 else self.url_next_page_num % vars()
        else:
            url = self.url_search % vars() if num == 1 else self.url_search_num % vars()

        # 2022-12-15 정성욱 추가
        # URL 연도 추가 작업
        timeFormat = "%Y-%m-%d"

        startDate = datetime.datetime.strptime(date_start, timeFormat)
        endDate = datetime.datetime.strptime(date_end, timeFormat)

        dateQuery = "&year="

        years = relativedelta(years=1)
        sd = startDate.year
        ed = endDate.year

        while sd != ed:
            dateQuery = dateQuery + endDate.strftime("%Y") + "%3A"
            endDate = endDate - years
            ed = endDate.year
        dateQuery = dateQuery + endDate.strftime("%Y")

        url = url + dateQuery
        return url
            
    # Returns a generator that yields URLs.
    # def naver_academic_search(query,  idx_num, stop, dir_id, num=1, start=0, pause=2.0):
    def search(
        self,
        query, 
        idx_num, 
        stop = 0, 
        date_start = '', 
        date_end = '', 
        dir_id = '0', 
        num = 1, 
        start = 0, 
        pause = 2.0,
        out_filepath=''):

        self.set_cookie_jar("academic")

        settings = self.get_settings("academic")
        stop = settings["max_count"]
        query1 =query
        # file_name ="/home/theimc/crawler/data/"

        query = urllib.parse.quote_plus(query,)

        url = self.get_search_url(query, date_start, date_end, num)

        now = time.localtime()
        uniq_file_name = str(now.tm_year) +"_"+ str(now.tm_mon) +"_"+ str(now.tm_mday) +"_"+ str(now.tm_hour) +"_"+ str(now.tm_min) +"_"+ str(now.tm_sec)
        out_file = open(out_filepath, 'a')

        out_count = 0
        count_web = 0
        html_status = 200
        while start < stop:

            settings = self.get_settings("academic")
            delay_time = settings["delay_time"]
            time.sleep(delay_time)
            
            # Request the Naver Search results page.
            try :
                html, html_status = self.get_page_with_session(url)
                if html_status != 200:
                    return creat_file_name, count_web, html_status
                    
                out_count = 0
            except Exception as err:
                out_count += 1
                log.debug(f"{err}... 페이지를 다시 호출합니다. ({out_count}/{stop})")
                if out_count == settings["out_max_count"] + 1:
                    start = stop
                
                #print "\nget_page() error"
                continue
            finally :
                # [2013-08-14]
                # Prepare the URL for the next request.
                if start < 1:
                    start += (num + 1)
                else:
                    start += num

            # Parse the response and process every anchored URL.
            soup_list = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
            list_html = soup_list('div', {'class' : 'ui_listing_info'})

            for li in list_html:
                try:
                    link = "http://academic.naver.com" + li("a")[0].get("href")
                except Exception as err:
                    log.debug(err)
                    link = ""

                try:
                    title_text = li("a")[0].text.strip()
                except Exception as err:
                    log.debug(err)
                    title_text = ""

                try:
                    contents_text = li("p")[0].text.strip().replace("\n", " ")
                except Exception as err:
                    log.debug(err)
                    contents_text = ""

                if title_text !="":
                    try:
                        scrape_text = title_text + '\t' + link +'\t'+ contents_text
                        out_file.write(scrape_text + '\n')
                        # log.debug(scrape_text[0:100])
                        count_web = count_web + 1
                        log.debug(f"task-[{idx_num}] 수집 중 => 키워드: {query1}, 카운트: {count_web}, 내용: {scrape_text[0:]}")
                    except Exception as err:
                        log.debug(err)
                        continue

                # time.sleep(1)
                url = self.get_search_url(query, date_start, date_end, num, start=start, is_next=True)

            if count_web > stop: break
            if len(list_html) < settings["unit_count"]: break

        try :
            out_file.close()
        except:
            pass

        return out_file.name, count_web, html_status
