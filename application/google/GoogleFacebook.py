from bs4 import BeautifulSoup
import os, time, urllib, urllib.request as urllib2
from earthling.service.Logging import log
from earthling.handler.earthling_dao import exec
from application.google.GoogleBase import GoogleBase

class GoogleFacebook(GoogleBase):
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

        settings = self.get_settings("facebook")
        stop = settings["max_count"]
        url_query = urllib.parse.quote_plus(query)
        start_date = date_start.split("-")[1] + "/" + date_start.split("-")[2] + "/" + date_start.split("-")[0]
        end_date = date_end.split("-")[1] + "/" + date_end.split("-")[2] + "/" + date_end.split("-")[0]
        out_file = open(out_filepath,"a")
        
        current_repeat_count = 0
        count_web = 0
        html_status = 200
        while True:
            url = 'https://www.google.com/search?q=' + url_query + '+site:facebook.com&newwindow=1&tbs=cdr:1,cd_min:' + start_date + ',cd_max:' + end_date + '&start=' + str(current_repeat_count * 10) + '&sa=N'

            html, html_status = self.get_page(url)
            if html_status != 200:
                break

            soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
            list_html = []
            try:
                list_html = soup('div', {'class' : 'g'})
            except Exception as err:
                log.debug(err)

            if list_html == []:
                break

            last_page_check = soup('p', {'id' : 'ofr'})

            for item in list_html:
                try:
                    title = item('h3')[0].text
                except:
                    title = ""

                try:
                    link = item('a')[0].get('href')
                except:
                    link = ""

                try:
                    text = item('div', {'class' : 'VwiC3b'})[0].text
                except:
                    text = ""

                try:
                    scrape_text = title + '\t' + link +'\t'+ text
                    out_file.write(scrape_text + '\n')
                    count_web = count_web + 1
                    log.debug(f"task-[{idx_num}] 수집 중 => 키워드: {query}, 카운트: {count_web}, 내용: {scrape_text[0:30]}")
                except Exception as err:
                    log.debug(err)
                    continue

            if len(last_page_check) > 0:
                break

            settings = self.get_settings("facebook")
            if count_web > settings["max_count"]:
                break

            repeat_count = settings["repeat_count"]
            if current_repeat_count > repeat_count:
                break
            
            current_repeat_count = current_repeat_count + 1
            delay_time = settings["delay_time"]
            log.debug(f"Trying... {current_repeat_count} / {repeat_count}.. Wait {delay_time} seconds")
            time.sleep(delay_time)

        try :
            out_file.close()
        except:
            pass
        
        return out_file.name, count_web, html_status


# When run as a script, take all arguments as a search query and run it.
if __name__ == "__main__":
    GoogleFacebook()
    # google_facebook_search('갤럭시', '342026', date_start='2022-04-01', date_end='2022-04-11')ssssssqwqwㅈㄷㅎㅈㄷㅎ