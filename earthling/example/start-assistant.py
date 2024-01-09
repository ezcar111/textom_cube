import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
print(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from connector.MySQLPoolConnector import *
# import os

# def action(task):
#     log.debug("바깥의 Custom Action으로 처리합니다!!")

# if __name__ == "__main__":

#     if not os.path.isdir("./temp"):
#         os.mkdir("./temp")
    
#     if not os.path.isdir("./logs"):
#         os.mkdir("./logs")

#     run(action)
