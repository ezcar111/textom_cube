import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from earthling.service.Logging import log
from earthling.handler.dao.BaseDAO import BaseDAO

from earthling.handler.dao.NaverDAO import NaverDAO
from earthling.handler.dao.GoogleDAO import GoogleDAO
from earthling.handler.dao.GoogleCnDAO import GoogleCnDAO
from earthling.handler.dao.DaumDAO import DaumDAO
from earthling.handler.dao.BaiduDAO import BaiduDAO

dao_class = {
    "naver": NaverDAO(),
    "google": GoogleDAO(),
    "googlecn": GoogleCnDAO(),
    "daum": DaumDAO(),
    "baidu": BaiduDAO()
}

from application.naver.NaverBase import NaverBase
from application.naver.NaverWeb import NaverWeb
from application.naver.NaverBlog import NaverBlog
from application.naver.NaverNews import NaverNews
from application.naver.NaverCafe import NaverCafe
from application.naver.NaverKin import NaverKin
from application.naver.NaverAcademic import NaverAcademic

from application.google.GoogleBase import GoogleBase
from application.google.GoogleWeb import GoogleWeb
from application.google.GoogleNews import GoogleNews
from application.google.GoogleFacebook import GoogleFacebook

from application.googlecn.GoogleCnBase import GoogleCnBase
from application.googlecn.GoogleCnWeb import GoogleCnWeb
from application.googlecn.GoogleCnAcademic import GoogleCnAcademic

from application.daum.DaumBase import DaumBase
from application.daum.DaumWeb import DaumWeb
from application.daum.DaumBlog import DaumBlog
from application.daum.DaumNews import DaumNews
from application.daum.DaumCafe import DaumCafe

from application.baidu.BaiduBase import BaiduBase
from application.baidu.BaiduWeb import BaiduWeb
from application.baidu.BaiduNews import BaiduNews
from application.baidu.BaiduAcademic import BaiduAcademic


data_class = {
    "naver": {
        "base": NaverBase(),  
        "web": NaverWeb(), 
        "blog": NaverBlog(), 
        "news": NaverNews(), 
        "cafe": NaverCafe(), 
        "kin": NaverKin(), 
        "academic": NaverAcademic()
    },

    "google": {
        "base": GoogleBase(),  
        "web": GoogleWeb(), 
        "news": GoogleNews(), 
        "facebook": GoogleFacebook()
    },

    "googlecn": {
        "base": GoogleCnBase(),  
        "web": GoogleCnWeb(), 
        "academic": GoogleCnAcademic()
    },

    "daum": {
        "base": DaumBase(),  
        "web": DaumWeb(), 
        "blog": DaumBlog(), 
        "news": DaumNews(), 
        "cafe": DaumCafe()
    },

    "baidu": {
        "base": BaiduBase(),  
        "web": BaiduWeb(), 
        "news": BaiduNews(), 
        "academic": BaiduAcademic()
    },
}


import pickle, yaml
if __name__ == "__main__":

    dao_settings = None
    with open("earthling/handler/dao/settings.yaml") as f:
        dao_settings = yaml.load(f, Loader=yaml.FullLoader)

        for channel in list(dao_settings.keys()):
            dao = None
            channel_setting = dao_settings.get(channel)
            dao_file_path = channel_setting.get("dao_file_path")
            dao = dao_class.get(channel)
            if dao is None:
                continue
            
            with open(dao_file_path, 'wb') as file:
                log.debug(dao_file_path)
                pickle.dump(dao, file)

    app_settings = None
    with open("application/settings.yaml") as f:
        app_settings = yaml.load(f, Loader=yaml.FullLoader)

        for channel in list(app_settings.keys()):
            dao = None
            channel_setting = app_settings.get(channel)            
            if "dict" not in str(type(channel_setting)):
                continue
            
            serialized_file_path = channel_setting.get("serialized_file_path")
            data_types = channel_setting.get("data_types")

            save_file_path = f"{serialized_file_path}/base.pickle"
            with open(save_file_path, 'wb') as ff:
                log.debug(save_file_path)
                target_data_class = data_class.get(channel).get("base")
                pickle.dump(target_data_class, ff)

            for data_type in data_types:
                target_data_class = data_class.get(channel).get(data_type)

                if target_data_class is None:
                    continue
                
                save_file_path = f"{serialized_file_path}/{data_type}.pickle"
                with open(save_file_path, 'wb') as ff:
                    log.debug(save_file_path)
                    pickle.dump(target_data_class, ff)