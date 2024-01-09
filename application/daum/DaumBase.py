import yaml, application.settings as settings, application.common as cmn
import urllib.request as urllib2
from earthling.service.Logging import log

class DaumBase:

    def get_page(self, url, with_cookie = False):
        # time.sleep(7)
        html, html_status = '', 200
        try:
            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE enviable; DAUMOA 2.0; DAUM Web Robot; Daum Communications Corp., Korea; +http://ws.daum.net/aboutkr.html)')
            request.add_header('Accept', 'text/html, application/xhtml+xml, */*')
            request.add_header('Accept-Language', 'ko-kr,ko;q=0.8,en-us;q=0.5,en;q=0.3')
            request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
            request.add_header('Keep-Alive', '115')
            request.add_header('Connection', 'keep-alive')

            if with_cookie: 
                self.cookie_jar.add_cookie_header(request)

            response = urllib2.urlopen(request)
            html_status = response.status
            if html_status == 200:

                if with_cookie: 
                    self.cookie_jar.extract_cookies(response, request)

                html = response.read()
            else:
                cmn.proc_html_status(html_status)
            
            response.close()

            if with_cookie: 
                self.cookie_jar.save()
        
        except Exception as err:
            log.debug(err)

        return html, html_status

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
        pass

    def get_url(self, keyword, date_start='', date_end='', start=0):
        pass

    def get_settings(self, data_type=''):
        return cmn.get_settings("daum", data_type)
        # log_file = settings.LOG_DATA_SAVE_PATH
        # app_sttings_path = settings.APP_SETTINGS_PATH
        # app_settings = None
        # with open(app_sttings_path) as f:
        #     app_settings = yaml.load(f, Loader=yaml.FullLoader)
        #     app_settings = app_settings['daum']
        #     if data_type != '':
        #         app_settings = app_settings.get(data_type)

        # return app_settings
    
    # def get_cookie_jar(self, data_type=''):
        # return cmn.get_cookie_jar("daum", data_type)
    
    def set_cookie_jar(self, data_type):
        self.cookie_jar = cmn.get_cookie_jar("daum", data_type)
        try:
            self.cookie_jar.load()
        except Exception:
            pass

    
    def monit_url(self, url):
        log.debug(f"[Messaging] 다음의 URL에서 콘텐츠를 수집합니다=> {url}")

    def monit_count(self, idx_num=0, query='', current_item_count=0, scrape_text=''):
        log.debug(f"task-[{idx_num}] 수집 중 => 키워드: {query}, 카운트: {current_item_count}, 내용: {scrape_text[0:30]}")

    def monit_current(self, current_repeat_count=1, max_repeat_count=10, current_item_count=0, max_item_count=1000, delay_time=2):
        log.debug(f"[Current Working] RepeatCount: {current_repeat_count}/{max_repeat_count}, Collection: {current_item_count}/{max_item_count}.. Wait {delay_time} seconds")

