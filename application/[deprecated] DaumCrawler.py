from application.BaseCrawler   import BaseCrawler
from application.daum.DaumWeb  import DaumWeb
from application.daum.DaumBlog import DaumBlog
from application.daum.DaumNews import DaumNews
from application.daum.DaumCafe import DaumCafe

from application.daum.DaumBase   import DaumBase
from earthling.handler.dao.DaumDAO import DaumDAO

class DaumCrawler(BaseCrawler):

    def __init__(self, dao):
        super().__init__("daum", DaumBase(), dao)
        
    def get_data_poly(self, data_type_name):
        data_type, poly = '', None
        if "web" in data_type_name:
            data_type = "web"
            poly = DaumWeb()

        elif "blog" in data_type_name:
            data_type = "blog"
            poly = DaumBlog()

        elif "news" in data_type_name:
            data_type = "news"
            poly = DaumNews()

        elif "cafe" in data_type_name:
            data_type = "cafe"
            poly = DaumCafe()
        
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