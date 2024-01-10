import os, sys, time
from selenium import webdriver
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from earthling.service.Logging import log
# import application.settings as settings
from application.naver.NaverBase import NaverBase

class NaverKin(NaverBase):

    def get_url(self, keyword, date_start='', date_end=''):

        date_start = date_start.replace("-","")
        date_end = date_end.replace("-","")

        if date_start == '' or date_end == '':
            url = "https://search.naver.com/search.naver?query="+str(keyword)+"&nso=&where=kin&sm=tab_jum"
        else:
            url = "https://search.naver.com/search.naver?where=kin&query="+str(keyword)+"&sm=tab_jum&nso=so%3Ar%2Ca%3Aall%2Cp%3Afrom"+(date_start)+"to"+(date_end)

        return url

    def getNextUrl(self, keyword, date_start='', date_end='', kin_start=21):

        date_start = date_start.replace("-","")
        date_end = date_end.replace("-","")

        if date_start == '' or date_end == '':        
            url = "https://search.naver.com/search.naver?where=kin&kin_display=10&qt=&title=0&&answer=0&grade=0&choice=0&sec=0&nso=so%3Ar%2Ca%3Aall%2Cp%3Aall&query="+str(keyword)+"&c_id=&c_name=&sm=tab_pge&kin_start="+str(kin_start)+"&kin_age=0"
        else:        
            url = "https://search.naver.com/search.naver?where=kin&kin_display=10&qt=&title=0&&answer=0&grade=0&choice=0&sec=0&nso=so%3Ar%2Ca%3Aall%2Cp%3Afrom" + date_start + "to" + date_end + "&query="+str(keyword)+"&c_id=&c_name=&sm=tab_pge&kin_start="+str(kin_start)+"&kin_age=0"
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
        # __init__
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_driver_path = self.get_chrome_driver_path()
        browser = webdriver.Chrome(chrome_driver_path, chrome_options=chrome_options)     
        
        date_start = date_start.replace('-', '')
        date_end   = date_end.replace('-', '')

        html_status = 200

        hashes = set()
        settings = self.get_settings("kin")
        kin_start = settings["unit_count"]
        
        count_web = 0
        stop_count = settings["max_count"]

        out_file = open(out_filepath, "a") #createFile()
        creat_file_name = out_file.name
        
        out_count = 0
        while True:        
            if count_web > stop_count:
                break

            settings = self.get_settings("kin")
            if kin_start > settings["max_count"]:
                break

            if kin_start == settings["unit_count"]:
                url = self.get_url(keyword, date_start, date_end)
            else:
                url = self.getNextUrl(keyword, date_start, date_end, kin_start)

            try:
                html_status = self.get_page(url, browser)
            except Exception as err:
                log.debug(f"err NaverKin_line88_{err}")
                html_status = 'error'
                return creat_file_name, count_web, html_status
            if html_status != 200:
                return creat_file_name, count_web, html_status

            time.sleep(2)                

            html_element = browser.page_source

            soup = BeautifulSoup(str(html_element), "html.parser", from_encoding="utf-8")
            
            for i in range(11):
                try:
                    a_link = soup.findAll("a",{"class":"api_txt_lines question_text"})[i]['href']
                    # Discard repeated results.
                    try :
                        h = hash(a_link)
                        if h in hashes:
                            continue
                        hashes.add(h)
                    except :
                        continue
                    out_count = 0
                except Exception as err:
                    out_count += 1
                    kin_out_max_count = settings["out_max_count"]
                    log.debug(f"{err}... 페이지를 다시 호출합니다. ({out_count}/{kin_out_max_count})")
                    if out_count == kin_out_max_count + 1:
                        kin_start = settings["max_count"]
                    break
                
                try:
                    title_text = soup.findAll("a",{"class":"api_txt_lines question_text"})[i].text
                    title_text = " ".join(title_text.split())                
                except:
                    title_text = ""            
                try:
                    content_text = soup.findAll("a",{"class":"api_txt_lines answer_text"})[i].text
                    content_text = " ".join(content_text.split())                
                except:
                    content_text = ""

                try:
                    scrape_text = title_text + '\t' + a_link +'\t'+ content_text
                    out_file.write(scrape_text + '\n')
                    log.debug(scrape_text[0:30])
                    count_web = count_web + 1
                except Exception as err:
                    log.debug(err)
                    continue
            
            kin_start += settings["unit_count"]
            log.debug(f"task-[{idx_num}] 수집 중 => 키워드: {keyword}, 기간: {date_start} ~ {date_end}, 카운트: {kin_start}")
            # TODO: 전체수집 개발           
                
        browser.quit()
        out_file.close()

        return creat_file_name, count_web, html_status
