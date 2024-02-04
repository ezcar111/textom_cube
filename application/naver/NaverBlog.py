import requests
from bs4 import BeautifulSoup
from urllib import parse
import pandas as pd
import random
import os, sys, time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# sys.path.append('/home/theimc/incubate/textom-cube/')
from selenium import webdriver
import warnings
from earthling.service.Logging import log
from application.naver.NaverBase import NaverBase


class NaverBlog(NaverBase):
    def make_default_frame(self):
        result_table = pd.DataFrame(columns=["date", "title", "contents", "url"])
        return result_table

    def get_blog_list(self, keyword, date_start, date_end, out_filepath):
        date_start = date_start.replace("-","")
        date_end = date_end.replace("-","")
        out_file = open(out_filepath, "a")
        creat_file_name = out_file.name
        start = 1
        count_web = 0
        settings = self.get_settings("blog")
        stop_count = settings["max_count"]
        link_list =[]
        stat =0

        # page_1
        referer_query = {
            'query': keyword,
            'ssc': 'tab.blog.all', 
            # 'where': 'blog',
            'sm': 'tab_opt'
        }
        referer_query_parse = parse.urlencode(referer_query, doseq=True)
        referer = "https://search.naver.com/search.naver?" + referer_query_parse

        url_query = {
            # 'where': 'blog',
            'ssc': 'tab.blog.all', 
            'query': keyword,
            'sm': 'tab_opt',
            'nso': f'so:r,p:from{date_start}to{date_end}'
                
        }
        url_query_parse = parse.urlencode(url_query, doseq=True)
        url = "https://search.naver.com/search.naver?" + url_query_parse
        headers = {
            "referer":referer,
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.57 Whale/3.14.133.23 Safari/537.36"
        }

        res = requests.get(url, headers=headers)
        html_status = res.status_code
        if html_status != 200:
            return creat_file_name, count_web, res.status_code
        soup = BeautifulSoup(res.text,"lxml")  
        
        # data_url = soup.find('div', attrs={'class':'review_loading _trigger_base'})['data-api']
        # nlu = data_url.split('nlu_query=')[1].split('&')[0]
        
        try :
            ul = soup.select("li.bx")
            for li in ul:
                try:
                    title = li.select_one(".title_link").get_text().strip()
                    # date = li.select_one(".sub").get_text().strip()[:-1].replace(".","-")
                    link = li.select_one(".title_link")["href"].replace("?Redirect=Log&logNo=","/")
                    contents = li.select_one(".dsc_area").get_text().strip()
                    if link in link_list:
                        stat += 1
                        continue
                    link_list.append(url.strip())
                    if "naver" in url:
                        scrape_text = title + '\t' + link +'\t'+ contents
                        out_file.write(scrape_text + '\n')
                        count_web = count_web + 1
                    start += 1
                    if start > settings["max_count"]:
                        if start > 2*settings["max_count"]:
                            break
                        elif count_web > settings["max_count"]:
                            break
                except AttributeError:
                    continue
        except AttributeError as er : 
            print(er)
            pass

        time.sleep(random.randint(3,5))

        # page_2: get_total_contents
        referer_query = {
            'ssc': 'tab.blog.all', 
            # 'where': 'blog',
            'query': keyword,
            'sm': 'tab_opt',
            'nso': f'so:r,p:from{date_start}to{date_end}'
        }
        referer_query_parse = parse.urlencode(referer_query, doseq=True)
        referer = "https://search.naver.com/search.naver?" + referer_query_parse
        url_query = {
            'ssc': 'tab.blog.all', 
            'where': 'blog',
            # 'sm': 'tab_pge',
            'sm': 'tab_jum',
            'api_type': '1',
            # 'api_type': '1',
            'query': keyword,
            'rev': '44',
            'start': '31',
            'dup_remove': '1',
            'nso': f'p:from{date_start}to{date_end}',
            'dkey': '0',
            'nx_search_query': keyword,
            'spq': '0',
            '_callback': 'viewMoreContents'
        }
        # 'nlu_query': nlu,
        url_query_parse = parse.urlencode(url_query, doseq=True)
        url = "https://s.search.naver.com/p/blog/search.naver?" + url_query_parse
        print("url164")
        print(url)
        headers = {
            "referer":referer,
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.57 Whale/3.14.133.23 Safari/537.36"
        }

        res = requests.get(url, headers=headers)
        total = int(res.text.strip().split("html")[0][28:-3])
        if total >= 1020:
            total = 1020
        print(f"{keyword} {date_start} {date_end} : {total}")
        time.sleep(random.randint(3,5))
        
        # page_N
        k=1

        for page in range(31,total,30):
            print(page)
            # print(int(round(page/total,1)*100))
            url_query = {
                'ssc': 'tab.blog.all', 
                # 'where': 'blog',
                'sm': 'tab_pge',
                'api_type': '1',
                'query': keyword,
                'rev': '44',
                'start': page,
                'dup_remove': '1',
                'nso': f'p:from{date_end}to{date_start}',
                'dkey': '0',
                'nx_search_query': keyword,
                'spq': '0',
                '_callback': 'viewMoreContents'
            }
            # 'nlu_query': nlu,
            url_query_parse = parse.urlencode(url_query, doseq=True)
            url = "https://s.search.naver.com/p/blog/search.naver?" + url_query_parse
            print(url)
            res = requests.get(url, headers=headers)
            html = res.text.strip()[18:-1].replace("\\","")
            html = '"""'+html.split("html")[1][4:]+'"""'    
            soup = BeautifulSoup(html,"lxml")   
            try :
                # ul = soup.select("li.bx")
                
                ul = soup.select("li.bx")
                for li in ul:
                    try:
                        title = li.select_one(".api_txt_lines").get_text().strip()
                        link = li.select_one(".api_txt_lines")["href"].replace("?Redirect=Log&logNo=","/")
                        contents = li.select_one(".total_dsc").get_text().strip()
                        if link in link_list:
                            stat += 1
                            continue
                        link_list.append(url.strip())
                        if "naver" in url:
                            scrape_text = title + '\t' + link +'\t'+ contents
                            out_file.write(scrape_text + '\n')
                            count_web = count_web + 1
                        start += 1
                        if start > settings["max_count"]:
                            if count_web == 1000:
                                break
                            if start > 2*settings["max_count"]:
                                break
                            elif count_web > settings["max_count"]:
                                break
                        
                    except AttributeError:
                        continue
            except AttributeError as er : 
                print(er)
                pass

            if k%10==0:
                time.sleep(random.randint(4,7))

            k+=1
        return creat_file_name, count_web, html_status


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


        result_table = self.make_default_frame()
                
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        creat_file_name, count_web, html_status = self.get_blog_list(keyword, date_start, date_end, out_filepath)

        return creat_file_name, count_web, html_status

if __name__=="__main__":
    data = {
        "keyword": '총선 +정의당', 
        "task_no": str(10), 
        "stop": 1000, 
        "date_start": '2023-08-01', 
        "date_end": '2023-09-01',
        "out_filepath": '/home/theimc/incubate/textom-cube/test_folder.nohup'
    }
    naver_news = NaverBlog()
    create_file_name, item_count, html_status = naver_news.search(
        data["keyword"], 
        idx_num = str(data["task_no"]), 
        stop=data["stop"], 
        date_start=data["date_start"], 
        date_end=data["date_end"],
        out_filepath = data["out_filepath"])
