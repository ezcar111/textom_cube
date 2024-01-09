import os, sys, yaml
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from earthling.service.ComAssistant import *
from earthling.service.Logging import log

import time, json, application.settings as settings
from handler.earthling_dao import get_dao, update_state_to_finish, get_collection_cond

# from application.crawler import get_crawler

# def get_crawler_factory(channel):
#     return get_crawler.factory

def set_directory(channel):
    log_file = settings.LOG_DATA_SAVE_PATH
    app_sttings_path = settings.APP_SETTINGS_PATH
    app_settings = None
    with open(app_sttings_path) as f:
        app_settings = yaml.load(f, Loader=yaml.FullLoader)
        app_settings = app_settings[channel]
        
    file_name = app_settings["scrap_data_save_path"]
    
    if not os.path.exists(log_file): os.makedirs(log_file)
    os.chmod(log_file, 0o777)
    
    if not os.path.exists(file_name): os.makedirs(file_name)
    os.chmod(file_name, 0o77)

def get_crawler(channel):
    crawler = None
    dao = get_dao(channel)
    from application.BaseCrawler import BaseCrawler
    crawler = BaseCrawler(channel, dao)

    # if channel == "naver":
    #     from application.BaseCrawler import NaverCrawler
    #     crawler = NaverCrawler(dao)
    
    # elif channel == "google":
    #     from application.GoogleCrawler import GoogleCrawler
    #     crawler = GoogleCrawler(dao)
    
    # elif channel == "daum":
    #     from application.DaumCrawler import DaumCrawler
    #     crawler = DaumCrawler(dao)
    return crawler

def action(message):

    task_no = message["task_no"]
    data_type = json.loads(message["message"])
    channel = data_type["channel"]
    data_type_name = data_type["data_type_name"]
    set_directory(channel)

    result = get_collection_cond(task_no, channel)
    row = result[0] if len(result) else None
    if row is not None:
        crawler = get_crawler(channel)
        crawler.factory(task_no, row, channel, data_type_name)
        update_state_to_finish(task_no, data_type_name, channel)
    else:
        # log.debug(f"다음의 쿼리에서 검색된 레코드가 없습니다 => {query}")
        log.debug(f"데이터베이스 접속 정보를 확인하세요. 개발? 운영?")
        log.debug(f"From cube-assistant.py")

if __name__ == "__main__":
    run(action)
