from application.BaseCrawler BaseCrawlerDa  import BaseCrawler
from application.baidu.BaiduWeb  import BaiduWeb
from application.baidu.BaiduNews import BaiduNews
from application.baidu.BaiduAcademic import BaiduAcademic

from application.baidu.BaiduBase   import BaiduBase
from earthling.handler.dao.BaiduDAO import BaiduDAO

class BaiduCrawler(BaseCrawler):

    def __init__(self, dao):
        super().__init__("Baidu", BaiduBase(), dao)
        
    def get_data_poly(self, data_type_name):
        data_type, poly = '', None
        if "web" in data_type_name:
            data_type = "web"
            poly = BaiduWeb()

        elif "news" in data_type_name:
            data_type = "news"
            poly = BaiduNews()

        elif "academic" in data_type_name:
            data_type = "academic"
            poly = BaiduAcademic()
        
        return data_type, poly

    def exec_search(self, poly, data):
        create_file_name, item_count = poly.search(
                data["keyword"], 
                idx_num = str(data["task_no"]), 
                stop=data["stop"], 
                date_start=(data["date_start"]), 
                date_end=(data["date_end"]),
                out_filepath = data["out_filepath"])

        return create_file_name, item_count