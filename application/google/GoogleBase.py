import yaml, application.settings as settings, application.common as cmn
import urllib.request as urllib2
from earthling.service.Logging import log
class GoogleBase:

    def get_page(self, url):
        # time.sleep(30)
        html = ''
        html_status = 200
        try:
            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.118 Whale/2.11.126.23 Safari/537.36')
            request.add_header('Accept', '*/*')
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

    def get_page_with_session(self, url, session):
        html = ''
        html_status = 200
        try:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
                'sec-ch-ua-mobile': '?0',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Whale/3.12.129.46 Safari/537.36',
            }

            # requests google page
            res = session.get(url, headers=headers)
            html_status = res.status_code
            log.debug(f"html_status: {html_status}")
            if html_status == 200:
                html = res.text
            else:
                cmn.proc_html_status(html_status)

        except Exception as err:
            log.debug(err)

        return html, html_status


    def search(self,
        query,
        idx_num,
        stop = 0,
        tld='co.kr', 
        lang='ko', 
        num=100, 
        start=0, 
        pause=5.0, 
        date_start='', 
        date_end='',
        out_filepath=''):
        pass

    def get_settings(self, data_type=''):
        return cmn.get_settings("google", data_type)
        # log_file = settings.LOG_DATA_SAVE_PATH
        # app_sttings_path = settings.APP_SETTINGS_PATH
        # app_settings = None
        # with open(app_sttings_path) as f:
        #     app_settings = yaml.load(f, Loader=yaml.FullLoader)
        #     app_settings = app_settings['google']
        #     if data_type != '':
        #         app_settings = app_settings.get(data_type)

        # return app_settings