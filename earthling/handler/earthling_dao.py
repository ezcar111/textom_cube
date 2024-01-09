import os, sys, time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import yaml, random, pickle
from .dao.BaseDAO import BaseDAO
from .dao.NaverDAO import NaverDAO
from .dao.GoogleDAO import GoogleDAO
from .dao.BaiduDAO import BaiduDAO
from .dao.DaumDAO import DaumDAO
from .earthling_db_pool import exec
# 해당 모듈을 추가하면 다른 곳에서 순환 종속 에러 발생할 수 잇음
from service.Logging import log


def get_dao(channel = ''):
    dao_list = []
    with open("earthling/handler/dao/settings.yaml") as f:
        dao_settings = yaml.load(f, Loader=yaml.FullLoader)    
        
        if channel != '':
            channel_setting = dao_settings.get(channel)
            dao_file_path = channel_setting.get("dao_file_path")
            with open(dao_file_path, 'rb') as file:
                dao = pickle.load(file)
            return dao

        for channel in list(dao_settings.keys()):
            dao = None
            channel_setting = dao_settings.get(channel)
            dao_file_path = channel_setting.get("dao_file_path")
            with open(dao_file_path, 'rb') as file:
                dao = pickle.load(file)
                dao_list.append(dao)
                
    return dao_list

def select_wait_task():
    daos = get_dao()
    random.shuffle(daos)
    # log.debug(daos)
    result = []
    for dao in daos:
        q_result = dao.select_wait_task()
        if "list" in str(type(q_result)):
            result = result + q_result
        time.sleep(1)
    return result

def update_state_to_wait(no, data_type_name, channel):
    dao = get_dao(channel)
    dao.update_state_to_wait(no, data_type_name)

def update_state_to_start(no, data_type_name, channel):
    dao = get_dao(channel)
    dao.update_state_to_start(no, data_type_name)

def update_state_to_finish(no, data_type_name, channel):
    dao = get_dao(channel)
    dao.update_state_to_finish(no, data_type_name)

def get_collection_cond(no, channel):
    dao = get_dao(channel)
    return dao.get_collection_cond(no)

def update_state_S_to_Y(channel):    
    dao = get_dao(channel)
    return dao.update_state_S_to_Y()
