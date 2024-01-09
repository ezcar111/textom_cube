import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import yaml
from handler.dao.BaseDAO import BaseDAO
from handler.earthling_db_pool import exec
# 해당 모듈을 추가하면 다른 곳에서 순환 종속 에러 발생할 수 잇음
from service.Logging import log 

class BaiduDAO(BaseDAO):
    
    def __init__(self):
        super().__init__("baidu")

    def select_wait_task(self):
        test_index_query = self.get_test_index_query()
        query = "SELECT X.* " \
                "FROM ( " \
                "  SELECT " \
                "    idx, (SELECT idx FROM keyword_list WHERE idx = keyword_list_idx) AS k_idx, " \
                "    web_data, news_data, academic_data " \
                "  FROM scraw_baidu_datainfo " \
                "  WHERE " \
                f"   {test_index_query} (web_data  = 'Y' OR news_data = 'Y' OR academic_data = 'Y') " \
                "  ORDER BY idx ASC " \
                ") AS X " \
                "WHERE X.k_idx IS NOT NULL AND X.k_idx > 0 LIMIT 10 "

        result = exec(query, country='cn')
        # log.debug(result)
        for item in result:
            item["channel"] = self.channel
            item["data_type_names"] = self.data_type_names
        return result

    def update_state_to_finish(self, no, data_type_name):
        try:
            self.update_state(no, data_type_name, 'N')
            query = f"SELECT keyword_list_idx, web_data, news_data, academic_data FROM scraw_baidu_datainfo WHERE idx={no}"
            result = exec(query, country='cn')
            if len(result) > 0:
                k_idx = result[0]["keyword_list_idx"]
                crawl_state = [
                    result[0]["web_data"],
                    result[0]["news_data"],
                    result[0]["academic_data"]
                ]

                if ('Y' not in crawl_state) and ('S' not in crawl_state):
                    query = f"UPDATE keyword_list SET baidu_status = 'merge' WHERE idx = {k_idx}"
                    exec(query, country='cn')
        except:
            pass