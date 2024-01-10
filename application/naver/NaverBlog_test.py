import warnings

# 경고 무시
warnings.filterwarnings("ignore", category=UserWarning)

import os, sys, time
from selenium import webdriver
from bs4 import BeautifulSoup


# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append('/home/theimc/incubate/textom-cube/')
from earthling.service.Logging import log
# import application.settings as settings
from application.naver.NaverBase import NaverBase

class NaverBlog(NaverBase):

    def get_url(self, keyword, date_start='', date_end=''):
        date_start = date_start.replace("-","")
        date_end = date_end.replace("-","")

        if date_start == '' or date_end == '':
            url = "https://search.naver.com/search.naver?query="+str(keyword)+"&nso=&where=blog&sm=tab_viw.all"
        else:
            url = "https://search.naver.com/search.naver?where=blog&query="+str(keyword)+"&sm=tab_opt&dup_remove=1&post_blogurl=&post_blogurl_without=&nso=so%3Ar%2Ca%3Aall%2Cp%3Afrom"+(date_start)+"to"+(date_end)
        print(url)
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
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_driver_path = self.get_chrome_driver_path()
        browser = webdriver.Chrome(chrome_driver_path,chrome_options=chrome_options)    

        url = self.get_url(keyword, date_start, date_end)
        out_file = open(out_filepath, "a") #createFile()
        creat_file_name = out_file.name

        html_status = self.get_page(url, browser)
        if html_status != 200:
            return creat_file_name, count_web, html_status

        time.sleep(2)

        last_height = browser.execute_script("return document.body.scrollHeight")

        scroll_count = 0 

        while True:
            
            if scroll_count > 100:
                break
            
            try:
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                new_height = browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            except Exception as e:
                print(e)
                time.sleep(2)
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                new_height = browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            time.sleep(2)
            scroll_count += 1
            log.debug(f"task-[{idx_num}] 수집 중 => 키워드: {keyword}, 기간: {date_start} ~ {date_end}, 카운트: {scroll_count}")
            
        try:
            html_element = browser.page_source
            soup = BeautifulSoup(str(html_element), "html.parser", from_encoding="utf-8")    

            count_web = 0
            settings = self.get_settings("blog")
            stop_count = settings["max_count"]
            link_list =[]
            stat =0
            list_html = soup.findAll('div', {'class' : 'total_wrap api_ani_send'})
            # list_html2 = soup.findAll('div', {'class' : 'view_wrap'})
            # print(list_html2)
            list_html2 = soup('ul', {'class' : 'lst_view _list_base'})[0]
            list_html2 = BeautifulSoup(str(list_html2),"html.parser")
            list_html_tmp = list_html2('li', {'class' : 'bx'})
            for temp_html in list_html_tmp:
                temp_html = BeautifulSoup(str(temp_html),"html.parser")
                print("temp_html")
                print(temp_html)
                if count_web == stop_count:
                    break
                
                if stat > 10:
                    break
            
                try:
                    a_link = temp_html('a', {'class' : 'title_link'})[0]['href']
                except:
                    break
                
                if a_link in link_list:
                        stat += 1
                        continue
                link_list.append(a_link.strip())
                print('4')
                try:
                    title_text = str(temp_html('a', {'class' : 'title_link'})[0].text).strip()             
                    title_text = str.join(' ', title_text.split())
                except:
                    title_text = ""
                try:
                    content_text = temp_html('a', {'class' : 'dsc_link'})[0].text       
                    content_text = str.join(' ', str(content_text).split())
                except:
                    content_text = ""

                try:
                    scrape_text = title_text + '\t' + a_link +'\t'+ content_text
                    print(scrape_text)
                    out_file.write(scrape_text + '\n')
                    # log.debug(scrape_text[0:100])
                    count_web = count_web + 1
                except Exception as err:
                    log.debug(err)
                    break


                # TODO: 전체수집 개발    
            print('3-1')
            # for temp_html in list_html:
            #     print(temp_html)
            #     temp_html = BeautifulSoup(str(temp_html),"html.parser")
            #     print("temp_html")
            #     print(temp_html)
            #     if count_web == stop_count:
            #         break
                
            #     if stat > 10:
            #         break
            
            #     try:
            #         a_link = temp_html("a",{"class":"api_txt_lines total_tit"})[0]['href']
            #     except:
            #         break
                
            #     if a_link in link_list:
            #             stat += 1
            #             continue
            #     link_list.append(a_link.strip())
            #     print('4')
            #     try:
            #         title_text = str(temp_html('a', {'class' : 'api_txt_lines total_tit'})[0].text).strip()             
            #         title_text = str.join(' ', title_text.split())
            #     except:
            #         title_text = ""
            #     try:
            #         content_text = temp_html("div",{"class":"api_txt_lines dsc_txt"})[0].text            
            #         content_text = str.join(' ', str(content_text).split())
            #     except:
            #         content_text = ""

            #     try:
            #         scrape_text = title_text + '\t' + a_link +'\t'+ content_text
            #         out_file.write(scrape_text + '\n')
            #         # log.debug(scrape_text[0:100])
            #         count_web = count_web + 1
            #     except Exception as err:
            #         log.debug(err)
            #         break


            #     # TODO: 전체수집 개발        
            print('5')
            browser.quit()
            out_file.close()
            print('6')
        except Exception as err:
            print(err)
            print(err)
            print(err)
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
    naver_news = NaverBlog()
    create_file_name, item_count, html_status = naver_news.search(
        data["keyword"], 
        idx_num = str(data["task_no"]), 
        stop=data["stop"], 
        date_start=data["date_start"], 
        date_end=data["date_end"],
        out_filepath = data["out_filepath"])

