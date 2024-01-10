import time, os, re, sys, pickle, application.common as cmn
import re
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# from application.naver.NaverBase   import NaverBase
# from application.google.GoogleBase  import GoogleBase
# from application.baidu.BaiduBase   import BaiduBase
# from earthling.handler.dao.NaverDAO import NaverDAO
# from earthling.handler.dao.GoogleDAO import GoogleDAO
# from earthling.handler.dao.BaiduDAO import BaiduDAO

from application.common import *
from earthling.service.Logging import log
from earthling.handler.earthling_es import insert_list_to_es

class BaseCrawler:

    def get_data_poly(self, channel, data_type):
        app_settings = cmn.get_settings(channel=channel)
        serialized_file_path = app_settings.get("serialized_file_path")
        poly_path = f"{serialized_file_path}/{data_type}.pickle"
        poly = None

        with open(poly_path, 'rb') as file:
            poly = pickle.load(file)
        return poly

    def exec_search(self, poly, data):
        try:
            create_file_name, item_count, html_status = poly.search(
                    data["keyword"], 
                    idx_num = str(data["task_no"]), 
                    stop=data["stop"], 
                    date_start=data["date_start"], 
                    date_end=data["date_end"],
                    out_filepath = data["out_filepath"])
        except Exception as err:
            log.debug(f"basecrawler 38 line error")
            create_file_name=''
            item_count=0
            html_status=500
        return create_file_name, item_count, html_status

    def __init__(self, channel, dao):
        self.channel = channel
        self.base = self.get_data_poly(channel, "base")
        self.dao = dao

    def factory(self, task_no, row, channel, data_type):
        if row == None:
            log.debug(f"task-[{task_no}]를 수집할 수 없습니다. KEYWORD_LIST 혹은 SCRAW_NAVER_DATAINFO 테이블에서 [{task_no}]를 확인하세요.")
            return

        app_settings = cmn.get_settings(channel=channel)
        table_name = app_settings["scrap_table_name"]

        keyword, date_start, date_end = row["keyword"], row["date_start"], row["date_end"]
        log.debug(f"수집정보 => 채널: {channel}, 유형: {data_type}, 키워드: {keyword}, 기간: {date_start} ~ {date_end}, 테이블: {table_name}")

        poly = self.get_data_poly(channel, data_type) 
        if poly is not None:
            self.dao.exec(f"UPDATE {table_name} SET {data_type}_starttime = now() where idx={task_no}")

            search_data = {
                "keyword": keyword, 
                "task_no": str(task_no), 
                "stop": 1000, 
                "date_start": date_start, 
                "date_end": date_end,
                "out_filepath": self.get_out_filepath(channel, data_type)
            }

            create_file_name, item_count, html_status = self.exec_search(poly, search_data)

            if html_status == 200:
                self.dao.exec(f"UPDATE {table_name} SET {data_type}_data = 'N', {data_type}_endtime = now() WHERE idx={task_no}")
                self.save(task_no, data_type, create_file_name, item_count)
                log.debug(f"데이터 수집을 정상적으로 완료하였습니다.")

            else:
                self.dao.exec(f"UPDATE {table_name} SET {data_type}_data = 'Y', {data_type}_endtime = now() WHERE idx={task_no}")
                log.debug(f"데이터 수집에 실패하였습니다. (HTML STATUS: {html_status})")
                app_settings = cmn.get_settings(channel=channel)
                penalty_delay_time = app_settings['penalty_delay_time']
                time.sleep(penalty_delay_time)
    
    def get_out_filepath(self, channel, data_type):
        app_settings = cmn.get_settings(channel=channel)
        scrap_data_save_path = app_settings["scrap_data_save_path"]
        now = time.localtime()
        uniq_file_name = str(now.tm_year) +"_"+ str(now.tm_mon) +"_"+ str(now.tm_mday) +"_"+ str(now.tm_hour) +"_"+ str(now.tm_min) +"_"+ str(now.tm_sec)
        file_path =f"{scrap_data_save_path}/{uniq_file_name}_file_{data_type}.txt"
        return file_path

    def get_es_index_name(self, channel):
        app_settings = cmn.get_settings(channel=channel)
        es_index_name = app_settings["es_index_name"]
        return es_index_name

    def get_channel_alias(self, channel):
        app_settings = cmn.get_settings(channel=channel)
        alias = app_settings["alias"]
        return alias

    def save(self, task_no, data_type, create_file_name, item_count):
        p = re.compile(f"""\n+""")
        app_settings = cmn.get_settings(self.channel)
        table_name = app_settings["scrap_table_name"]
        result = self.dao.exec(f"SELECT keyword_list_idx from {table_name} where idx = {task_no}")
        row = result[0] if len(result) > 0 else None
        if row is not None:
            es_index_name = self.get_es_index_name(self.channel)
            channel_alias = self.get_channel_alias(self.channel)
            k_idx = row["keyword_list_idx"]
            out_file = open(create_file_name, 'r')
            data_list = []
            for lines in out_file:
                line = lines.split("\t")
                
                try :
                    title = str(line[0]).strip()
                except Exception as err:
                    # log.debug(err)
                    title = ""
                try:
                    url = str(line[1]).strip()
                except Exception as err:
                    # log.debug(err)
                    url = ""
                try :
                    text = str(line[2]).strip()
                    re_text = p.sub(" ", text)
                except Exception as err:
                    # log.debug(err)
                    text = ""
                    re_text = ""
                
                target = {
                    'idx'          : str(k_idx).strip(),
                    'kind'         : channel_alias,
                    'subKind'      : str(data_type).strip(),
                    'title'        : str(title).strip(),
                    'url'          : str(url).strip(),
                    'text'         : str(re_text).strip()
                }
                data_list.append(target)
                
                try:  
                    if len(data_list) > 100:
                        insert_list_to_es(data_list, es_index_name, "channel")
                        data_list = []
                        log.debug(f"task-[{task_no}]의 ({len(data_list)})개의 데이터가 ES에 저장되었습니다.")
                except:
                    pass
             
            try :
                
                if len(data_list) > 0:
                    insert_list_to_es(data_list, es_index_name, "channel")
                    log.debug(f"task-[{task_no}]의 ({len(data_list)})개의 데이터가 ES에 저장되었습니다.")
            except Exception as err:
                log.debug(err)
                pass

            out_file.close()
            self.dao.exec(f"UPDATE {table_name} SET {data_type}_countnum_craw={item_count} WHERE idx = {task_no}")

            try :
                nsize = os.path.getsize(create_file_name)
                result = self.dao.exec(f"SELECT user_id, date_start, date_end, keyword from keyword_list where idx ={k_idx}")
                row_user = result[0] if len(result) > 0 else None # cursor.fetchone()
                if row_user is not None:
                    user_id, date_start, date_end, keyword = row_user["user_id"], row_user["date_start"], row_user["date_end"], row_user["keyword"].replace("'", "''")
                    file_size = float(nsize/1024)
                    query = "INSERT INTO scrw_use_size (" \
                            "  keyword_idx, keyword, user_id, channel, sub_channel, scrw_size, start_date, end_date, site_kind" \
                            ") VALUES (" \
                            f"{k_idx}, '{re.escape(keyword)}', '{user_id}', '{channel_alias}', '{data_type}', {file_size}, '{date_start}', '{date_end}', 'channel'" \
                            ")"
                    # log.debug(query)
                    self.dao.exec(query)

            except Exception as err:
                log.debug(err)
                pass

            try:
                os.remove(create_file_name)
            except Exception as err:
                log.debug(err)
                pass