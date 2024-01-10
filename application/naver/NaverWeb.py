import os, sys, time
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from earthling.service.Logging import log
# import application.settings as settings
from application.naver.NaverBase import NaverBase
from datetime import datetime, timedelta

class NaverWeb(NaverBase):

    def get_url(self, keyword, date_start='', date_end='', start=0):
        date_start = date_start.replace("-","")
        date_end = date_end.replace("-","")

        if date_start == '' or date_end == '':
            url = "https://search.naver.com/search.naver?query="+str(keyword)+"&nso=&where=web&sm=tab_viw.all"
        else:
            # url = "https://search.naver.com/search.naver?query="+str(keyword)+"&sm=tab_opt&dup_remove=1&post_blogurl=&post_blogurl_without=&start="+str(start)+"&nso=so%3Ar%2Ca%3Aall%2Cp%3Afrom"+(date_start)+"to"+(date_end)
            url = "https://search.naver.com/search.naver?where=web&query="+str(keyword)+"&sm=tab_opt&dup_remove=1&post_blogurl=&post_blogurl_without=&start="+str(start)+"&nso=so%3Ar%2Ca%3Aall%2Cp%3Afrom"+(date_start)+"to"+(date_end)
        return url

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

        now = datetime.now()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_driver_path = self.get_chrome_driver_path()
        browser = webdriver.Chrome(chrome_driver_path,chrome_options=chrome_options) 
        start = 0

        d_start = datetime.strptime(date_start, "%Y-%m-%d")
        d_end = datetime.strptime(date_end, "%Y-%m-%d")
        dates = [(d_start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((d_end-d_start).days+1)]
        dates = sorted(dates, reverse=True)

        date_start = date_start.replace('-', '')
        date_end   = date_end.replace('-', '')

        out_file =  open(out_filepath, "a") #createFile()
        creat_file_name = out_file.name

        # count = 0

        fin = False
        count_web = 0

        # while True:
        total_date_count = len(dates)
        for tar_date in dates:
            
            start = 1
            while True:

                url = self.get_url(keyword, tar_date, tar_date, start)
                
                # print(url)
                try:
                    html_status = self.get_page(url, browser)
                except Exception as err:
                    log.debug(f"err NaverWeb_line76_{err}")
                    html_status = 'error'
                    return creat_file_name, count_web, html_status
                if html_status != 200:
                    return creat_file_name, count_web, html_status


                time.sleep(2)
                html_element = browser.page_source
                soup = BeautifulSoup(str(html_element), "html.parser", from_encoding="utf-8")
                
                settings = self.get_settings("web")
                web_list = soup.findAll("div", {"class" : "total_wrap"})

                try:
                    if len(web_list) == 0:
                        log.debug(f"[{tar_date}]의 데이터가 존재하지 않습니다.")
                        total_date_count -= 1
                        break
                except:
                    log.debug(f"[{tar_date}]의 데이터가 존재하지 않습니다.")
                    total_date_count -= 1
                    break

                for i in web_list:
                    # count = count + 1
                    try:
                        a_link = i.find("a", {"class" : "link_tit"}).get('href')
                    except:
                        a_link = ""
                        
                    try:
                        title_text = i.find("a", {"class" : "link_tit"}).text.strip()
                    except:
                        title_text = ""
                        
                    try:
                        content_text = i.find("div", {"class" : "api_txt_lines"}).text.strip()
                    except:
                        content_text = ""
                            

                    try:
                        if count_web >= settings["max_count"]:
                            log.debug(f"수집 개수가 [{count_web}]개에 도달하여 수집을 종료합니다.")
                            fin = True
                            break
                        
                        count_web = count_web + 1
                        scrape_text = title_text + '\t' + a_link +'\t'+ content_text
                        out_file.write(scrape_text + '\n')
                    except Exception as err:
                        log.debug(err)
                        continue

                
                total_max_count = settings["max_count"]                
                web_unit_count = settings["unit_count"]
                unit_max_count = settings["max_count"] / total_date_count
                start = start + web_unit_count
                if len(web_list) < web_unit_count: 
                    log.debug(f"task-[{idx_num}] 수집 중 => 키워드: {keyword}, 기간: {date_start} ~ {date_end}, 카운트:  {count_web} / {total_max_count}, (인덱스: {start})")
                    break
                
                if start >= unit_max_count: 
                    log.debug(f"task-[{idx_num}] 수집 중 => 키워드: {keyword}, 기간: {date_start} ~ {date_end}, 카운트:  {count_web} / {total_max_count}, (인덱스: {start})")
                    break

                log.debug(f"task-[{idx_num}] 수집 중 => 키워드: {keyword}, 기간: {date_start} ~ {date_end}, 카운트:  {count_web} / {total_max_count}, (인덱스: {start})")


            if fin:
                break
                
        browser.quit()
        out_file.close()

        return creat_file_name, count_web, html_status