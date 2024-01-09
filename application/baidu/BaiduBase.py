import re, time
import urllib, urllib.request as urllib2
from bs4 import BeautifulSoup
import time, yaml, application.settings as settings, datetime
from selenium import webdriver
from earthling.service.Logging import log

class BaiduBase:

    def __init__(self, data_type=''):
        self.data_type = data_type

    def get_page(self, url):
        html = ''
        html_status = 200
        try:
            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.118 Whale/2.11.126.23 Safari/537.36')
            request.add_header('Accept', '*/*')
            request.add_header('Cache-Control', 'no-cache')
            request.add_header('Accept-Language', 'ko-kr,ko;q=0.8,en-us;q=0.5,en;q=0.3')
            request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
            request.add_header('Connection', 'keep-alive')
            response = urllib2.urlopen(request)
            html_status = response.status
            if html_status == 200:
                html = response.read()
            response.close()
        except Exception as err:
            log.debug(err)

        return html, html_status


    def get_html_list(self, soup):
        html_list = []
        return html_list


    def get_resource(self, item):
        title, link, body = '', '', ''
        return title, link, body


    def search(self, 
            query, 
            idx_num, 
            stop=1000,
            date_start='', 
            date_end='', 
            out_filepath=''):

        settings = self.get_settings(self.data_type)
        stop = settings["max_count"]

        crawl_count = 0
        page_count = 0
        break_flag = False
        p = re.compile(" {2,}")

        out_file = open(out_filepath, "a") #createFile(channel)
        html_status = 200
        while True:
            url = self.get_url(query, page_count, date_start, date_end)
            self.monit_url(url)

            html, html_status = self.get_page(url)
            if html_status != 200:
                return out_file.name, crawl_count, html_status

            soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
            html_list = self.get_html_list(soup)
            if len(html_list) == 0:
                break

            for item in html_list:
                title, link, body = self.get_resource(item)
                scrape_text = title + '\t' + link +'\t'+ body
                out_file.write(scrape_text + '\n')
                crawl_count = crawl_count + 1

                self.monit_count(
                    idx_num=idx_num, 
                    query=query, 
                    current_item_count=crawl_count, 
                    scrape_text=scrape_text
                )

                if crawl_count >= stop:
                    break_flag = True
                    break

            settings = self.get_settings(self.data_type)
            stop = settings["max_count"]
            unit_count = settings["unit_count"]
            delay_time = settings["delay_time"]

            if page_count > stop:
                print("return first page")
                break

            if break_flag == True:
                print("break_flag break")
                break

            if crawl_count < 2:
                print("html_count break")
                break

            page_count = page_count + unit_count

            time.sleep(delay_time)
            self.monit_current(
                current_repeat_count=page_count / 10, 
                max_repeat_count=stop / 10, 
                current_item_count=crawl_count, 
                max_item_count=stop, 
                delay_time=10
            )

        try:
            out_file.close()
        except:
            pass
            
        return out_file.name, crawl_count, html_status
    

    def get_url(self, keyword, page_count, start='', end=''):
        pass


    def get_settings(self, data_type=''):
        log_file = settings.LOG_DATA_SAVE_PATH
        app_sttings_path = settings.APP_SETTINGS_PATH
        app_settings = None
        with open(app_sttings_path) as f:
            app_settings = yaml.load(f, Loader=yaml.FullLoader)
            app_settings = app_settings['baidu']
            if data_type != '':
                app_settings = app_settings.get(data_type)

        return app_settings


    def monit_url(self, url):
        log.debug(f"[Messaging] 다음의 URL에서 콘텐츠를 수집합니다=> {url}")


    def monit_count(self, idx_num=0, query='', current_item_count=0, scrape_text=''):
        log.debug(f"task-[{idx_num}] 수집 중 => 키워드: {query}, 카운트: {current_item_count}, 내용: {scrape_text[0:30]}")


    def monit_current(self, current_repeat_count=1, max_repeat_count=10, current_item_count=0, max_item_count=1000, delay_time=2):
        log.debug(f"[Current Working] Repeat: {current_repeat_count}/{max_repeat_count}, Collection: {current_item_count}/{max_item_count}.. Wait {delay_time} seconds")

