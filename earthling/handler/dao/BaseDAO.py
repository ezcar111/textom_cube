import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import yaml
from handler.earthling_db_pool import exec as pool_exec
# 해당 모듈을 추가하면 다른 곳에서 순환 종속 에러 발생할 수 잇음
from service.Logging import log 

class BaseDAO:

    def set_country(self):
        cn_channel_list = ["baidu", "googlecn"]
        if self.channel in cn_channel_list:
            self.country = "cn"
        else:
            self.country = "kr"

    def __init__(self, channel):
        self.channel = channel
        self.set_country()

        self.app_settings = None
        with open("earthling/handler/dao/settings.yaml") as f:
            self.app_settings = yaml.load(f, Loader=yaml.FullLoader)
            self.app_settings = self.app_settings[channel]

        self.data_type_names = self.app_settings["data_type_names"]
        self.test_index = self.app_settings["test_index"]
        self.scraw_table_name = self.app_settings["scraw_table_name"]
        self.scraw_status_name = self.app_settings["scraw_status_name"]
        self.scraw_channel_name = self.app_settings["scraw_channel_name"]
    
    def get_host_ip(self):
        host = ''
        with open(f'earth-compose.yml') as f:
            compose = yaml.load(f, Loader=yaml.FullLoader)
            host = compose['rpc']['host']
        return host['address']

    def get_test_index_query(self):
        if self.test_index > 0:
            return f"idx = {self.test_index} AND "
        return ''

    def select_wait_task(self):
        pass
    
    def update_state(self, no, data_type_name, state):
        query = f"UPDATE {self.scraw_table_name} SET {data_type_name}_data = '{state}' WHERE idx = {no}"
        self.exec(query)

    def get_keyword_list_index(self, no):
        query = f"SELECT keyword_list_idx FROM {self.scraw_table_name} WHERE idx={no}"
        result = self.exec(query)
        return result
    
    def update_keyword_list_to_extract(self, k_idx):
        query = f"UPDATE keyword_list SET {self.scraw_status_name} = 'extract' WHERE idx = {k_idx}"
        self.exec(query)
    
    def update_state_to_wait(self, no, data_type_name):
        result = self.get_keyword_list_index(no)
        if len(result) > 0:
            k_idx = result[0]["keyword_list_idx"]
            self.update_keyword_list_to_extract(k_idx)
            self.update_state(no, data_type_name, 'Y')

    def update_state_to_start(self, no, data_type_name):
        mng_addr = ''
        with open(f'earth-compose.yml') as f:
            compose = yaml.load(f, Loader=yaml.FullLoader)
            mng_addr = compose['rpc']['manager']['address']

        query = f"SELECT keyword_list_idx FROM {self.scraw_table_name} WHERE idx={no}"
        result = self.exec(query)
        if len(result) > 0:
            k_idx = result[0]["keyword_list_idx"]
            query = f"UPDATE keyword_list SET {self.scraw_status_name} = 'extract', {self.scraw_channel_name}_search_ip='{str(mng_addr)}' WHERE idx = {k_idx}"
            self.exec(query)
            self.update_state(no, data_type_name, 'S')

    def update_state_to_finish(self, no, data_type_name):
        pass
    
    def get_collection_cond(self, task_no):
        query=  f"SELECT " \
                f"  A.idx, KL.date_start, KL.date_end, KL.keyword " \
                f"FROM ( " \
                f"  SELECT idx, keyword_list_idx FROM {self.scraw_table_name} WHERE idx = {task_no} " \
                f") AS A " \
                f"JOIN keyword_list AS KL ON KL.idx = A.keyword_list_idx"

        result = self.exec(query)
        return result

    def update_state_S_to_Y(self):
        for name in self.data_type_names:
            query = f"UPDATE {self.scraw_table_name} SET {name}_data = 'Y' WHERE {name}_data = 'S'"
            self.exec(query)

    def exec(self, query):
        return pool_exec(query, country=self.country)
