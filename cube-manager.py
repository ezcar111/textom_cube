import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from earthling.service.ComManager import *
from earthling.handler.earthling_db_pool import exec
from earthling.handler.earthling_dao import update_state_S_to_Y
if __name__ == "__main__":

    # 매니저가 재시작되면 진행중이었던 것들은 상태가 Y로 변경 됨
    # channels = ["naver", "google"]
    # for channel in channels:
    #     update_state_S_to_Y(channel)
        
    run()