import os, sys, time
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
sys.path.append('/home/theimc/incubate/textom-cube/')
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from earthling.service.Logging import log
# import application.settings as settings
from application.naver.NaverBase import NaverBase
import requests

class NaverNews(NaverBase):
    
    def get_url(self, keyword, date_start='', date_end='', start=0):
        date_start = date_start.replace("-","")
        date_end = date_end.replace("-","")

        if date_start == '' or date_end == '':
            url = "https://search.naver.com/search.naver?query="+str(keyword)+"&nso=&where=news&sm=tab_viw.all"
        else:
            url = "https://search.naver.com/search.naver?where=news&query="+str(keyword)+"&sm=tab_opt&dup_remove=1&post_blogurl=&post_blogurl_without=&start="+str(start)+"&nso=so%3Ar%2Ca%3Aall%2Cp%3Afrom"+(date_start)+"to"+(date_end)

        return url

    # 메인 함수
    def search(
        self,
        keyword, 
        idx_num, 
        stop = 0, 
        date_start = '', 
        date_end = '', 
        dir_id = '0', 
        num = 1, 
        start = 0, 
        pause = 2.0,
        out_filepath=''):
        # __init__
        now = datetime.now()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_driver_path = self.get_chrome_driver_path()
        browser = webdriver.Chrome(chrome_driver_path,chrome_options=chrome_options)
        start = 0
        count_web = 0

        date_start = date_start.replace('-', '')
        date_end   = date_end.replace('-', '')
        
        out_file = open(out_filepath, "a") #createFile()
        creat_file_name = out_file.name
        url = self.get_url(keyword, date_start, date_end, start)
        try:
            html_status = self.get_page(url, browser)
        except Exception as err:
            log.debug(f"err NaverNews_line58_{err}")
            html_status = 'error'
            return creat_file_name, count_web, html_status
            
        if html_status != 200:
            return creat_file_name, count_web, html_status

        start = 1
        count = 0
        link_list =[]
        stat = 0
        while True:
            time.sleep(2)
            html_element = browser.page_source
            soup = BeautifulSoup(str(html_element), "html.parser", from_encoding="utf-8")
            
            list_html = soup.findAll('div', {'class' : 'news_wrap api_ani_send'})

            for temp_html in list_html:
                count = count + 1
                try:
                    a_link = temp_html("a", {"class" : "news_tit"})[0]['href']
                except:
                    a_link = ""

                if a_link in link_list:
                    stat += 1
                    continue
                link_list.append(a_link.strip())
                
                try:
                    title_text = str(temp_html("a", {"class" : "news_tit"})[0].text).strip()
                    #title_text = " ".join(title_text.split()) 
                    title_text = str.join(' ', str(title_text).split())
                except:
                    title_text = ""

                try:
                    content_text = temp_html("div", {"class" : "news_dsc"})[0].text.strip()
                    #content_text = " ".join(content_text.split())      
                    content_text = str.join(' ', str(content_text).split())
                except:
                    content_text = ""                      
                try:
                    press = temp_html("a", {"class": "info press"})[0].text.strip()
                    press = str.join(' ', str(press).split())
                except Exception as err:
                    print(err)
                    press = ""
                try:
                    scrape_text = title_text + '\t' + a_link +'\t'+ content_text +'\t'+ press
                    # scrape_text = title_text + '\t' + a_link +'\t'+ content_text
                    # log.debug(f"Count: {len(list_html)}, {scrape_text[0:30]}")
                    out_file.write(scrape_text + '\n')
                    count_web = count_web + 1
                except Exception as err:
                    log.debug(err)
                    continue
                settings = self.get_settings("news")
                if count_web > settings["max_count"]:
                    break

            settings = self.get_settings("news")
            news_unit_count = settings["unit_count"]
            start = start + news_unit_count
            if len(list_html) < news_unit_count: break
            # if start > settings["max_count"]: break
            if start > settings["max_count"]:
                if count_web > settings["max_count"]:
                    break
                elif start > 2*settings["max_count"]:
                    break
            
            url = self.get_url(keyword, date_start, date_end, start)
            html_status = self.get_page(url, browser, 0)
            if html_status != 200:
                return creat_file_name, count_web, html_status
            

            log.debug(f"task-[{idx_num}] 수집 중 => 키워드: {keyword}, 기간: {date_start} ~ {date_end}, 카운트: {start}")

            # TODO: 전체수집 개발        

            
        
        browser.quit()
        out_file.close()

        return creat_file_name, count_web, html_status

if __name__ == "__main__":
    # data = {
    #     "keyword": '전주한옥마을+경관', 
    #     "task_no": str(10), 
    #     "stop": 1000, 
    #     "date_start": '2020-09-07', 
    #     "date_end": '2020-09-13',
    #     "out_filepath": '/home/theimc/incubate/textom-cube/test_folder'
    # }
    data = {
        "keyword": '총선 +정의당', 
        "task_no": str(10), 
        "stop": 1000, 
        "date_start": '2023-08-01', 
        "date_end": '2023-08-31',
        "out_filepath": '/home/theimc/incubate/textom-cube/test_folder'
    }
    naver_news = NaverNews()
    create_file_name, item_count, html_status = naver_news.search(
        data["keyword"], 
        idx_num = str(data["task_no"]), 
        stop=data["stop"], 
        date_start=data["date_start"], 
        date_end=data["date_end"],
        out_filepath = data["out_filepath"])
