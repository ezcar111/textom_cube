
import os, sys, time, requests, re, yaml
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import application.settings  as settings
from earthling.service.Logging import log 
from earthling.handler.earthling_dao import exec
from earthling.handler.earthling_es import insert_list_to_es
from application.google.GoogleBase  import GoogleBase
from application.google.GoogleWeb  import GoogleWeb
from application.google.GoogleNews import GoogleNews
from application.google.GoogleFacebook import GoogleFacebook
from time import gmtime, strftime


def get_app_settings():
    base = GoogleBase()
    return base.getSettings()

def factory(task_no, row, data_type_name):
    if row == None:
        log.debug(f"task-[{task_no}]를 수집할 수 없습니다. KEYWORD_LIST 혹은 scraw_google_datainfo 테이블에서 [{task_no}]를 확인하세요.")
        return

    keyword, date_start, date_end = row["keyword"], row["date_start"], row["date_end"]
    log.debug(f"수집정보 => 키워드: {keyword}, 기간: {date_start} ~ {date_end}, 유형: {data_type_name}")

    data_type, google_poly = get_data_poly(data_type_name) 
    if google_poly is not None:
        exec(f"UPDATE scraw_google_datainfo SET {data_type}_starttime = now() where idx={task_no}")

        out_filepath = get_out_filepath(data_type)
        create_file_name, item_count = google_poly.search(
            keyword, 
            idx_num = str(task_no), 
            stop=1000, 
            date_start=date_start, 
            date_end=date_end,
            out_filepath = out_filepath)

        exec(f"UPDATE scraw_google_datainfo SET {data_type}_endtime = now() where idx={task_no}")
        save(task_no, data_type, create_file_name, item_count)


def get_data_poly(data_type_name):
    data_type, google_poly = '', None
    if "web" in data_type_name:
        data_type = "web"
        google_poly = GoogleWeb()

    elif "news" in data_type_name:
        data_type = "news"
        google_poly = GoogleNews()

    elif "facebook" in data_type_name:
        data_type = "facebook"
        google_poly = GoogleFacebook()
    
    return data_type, google_poly


def get_out_filepath(data_type):
    app_settings = get_app_settings()
    scrap_data_save_path = app_settings["SCRAP_DATA_SAVE_PATH"]
    now = time.localtime()
    uniq_file_name = str(now.tm_year) +"_"+ str(now.tm_mon) +"_"+ str(now.tm_mday) +"_"+ str(now.tm_hour) +"_"+ str(now.tm_min) +"_"+ str(now.tm_sec)
    file_path = f"{scrap_data_save_path}/{uniq_file_name}_google_{data_type}.txt"
    return file_path


def save(task_no, data_type, create_file_name, item_count):
    result = exec(f"SELECT keyword_list_idx from scraw_google_datainfo where idx = {task_no}")
    row = result[0] if len(result) > 0 else None
    if row is not None:
        k_idx = row["keyword_list_idx"]
        out_file = open(create_file_name, 'r')
        data_list = []
        for lines in out_file:
            line = lines.split("\t")

            try :
                title = str(line[0]).strip()
            except:
                title = ""
            try:
                url = str(line[1]).strip()
            except:
                url = ""
            try :
                text = str(line[2]).strip()
            except:
                text = ""

            target = {
                'idx'          : str(k_idx).strip(),
                'kind'         : str("google").strip(),
                'subKind'      : str(data_type).strip(),
                'title'        : str(title).strip(),
                'url'          : str(url).strip(),
                'text'         : str(text).strip(),                
            }
            data_list.append(target)
            
            try:  
                if len(data_list) > 100:
                    insert_list_to_es(data_list, "textom_data", str('channel'))
                    data_list = []
                    log.debug(f"task-[{task_no}]의 ({len(data_list)})개의 데이터가 ES에 저장되었습니다.")
            except:
                pass

        try :
            
            if len(data_list) > 0:
                insert_list_to_es(data_list, "textom_data", str('channel'))
                log.debug(f"task-[{task_no}]의 ({len(data_list)})개의 데이터가 ES에 저장되었습니다.")
        except Exception as err:
            log.debug(err)
            pass

        out_file.close()
        exec(f"UPDATE scraw_google_datainfo SET {data_type}_countnum_craw={item_count} WHERE idx = {task_no}")

        try :
            nsize = os.path.getsize(create_file_name)
            result = exec(f"SELECT user_id, date_start, date_end, keyword from keyword_list where idx ={k_idx}")
            row_user = result[0] if len(result) > 0 else None # cursor.fetchone()
            if row_user is not None:
                user_id, date_start, date_end, keyword = row_user["user_id"], row_user["date_start"], row_user["date_end"], row_user["keyword"]
                file_size = float(nsize/1024)
                query = "INSERT INTO scrw_use_size (" \
                        "  keyword_idx, keyword, user_id, channel, sub_channel, scrw_size, start_date, end_date, site_kind" \
                        ") VALUES (" \
                        f"{k_idx}, '{re.escape(keyword)}', '{user_id}', 'google', '{data_type}', {file_size}, '{date_start}', '{date_end}', 'channel'" \
                        ")"
                exec(query)

        except Exception as err:
            log.debug(err)
            pass

        try:
            os.remove(create_file_name)
        except Exception as err:
            log.debug(err)
            pass
        
if __name__ == "__main__":
    daemon_run()