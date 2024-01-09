from application.BaseCrawler   import BaseCrawler
from application.naver.NaverWeb  import NaverWeb
from application.naver.NaverBlog import NaverBlog
from application.naver.NaverNews import NaverNews
from application.naver.NaverCafe import NaverCafe
from application.naver.NaverKin import NaverKin
from application.naver.NaverAcademic import NaverAcademic

from application.naver.NaverBase   import NaverBase
from earthling.handler.dao.NaverDAO import NaverDAO

class NaverCrawler(BaseCrawler):

    def __init__(self, dao):
        super().__init__("naver", NaverBase(), dao)
        
    def get_data_poly(self, data_type_name):
        data_type, naver_poly = '', None
        if "web" in data_type_name:
            data_type = "web"
            naver_poly = NaverWeb()

        elif "blog" in data_type_name:
            data_type = "blog"
            naver_poly = NaverBlog()

        elif "news" in data_type_name:
            data_type = "news"
            naver_poly = NaverNews()

        elif "cafe" in data_type_name:
            data_type = "cafe"
            naver_poly = NaverCafe()

        elif "kin" in data_type_name:
            data_type = "kin"
            naver_poly = NaverKin()    

        elif "academic" in data_type_name:
            data_type = "academic"
            naver_poly = NaverAcademic()    
        
        return data_type, naver_poly

    def exec_search(self, poly, data):
        create_file_name, item_count, html_status = poly.search(
                data["keyword"], 
                idx_num = str(data["task_no"]), 
                stop=data["stop"], 
                date_start=(data["date_start"]), 
                date_end=(data["date_end"]),
                out_filepath = data["out_filepath"])

        return create_file_name, item_count, html_status