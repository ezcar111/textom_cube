from application.BaseCrawler   import BaseCrawler
from application.google.GoogleWeb  import GoogleWeb
from application.google.GoogleNews import GoogleNews
from application.google.GoogleFacebook import GoogleFacebook

from application.google.GoogleBase  import GoogleBase
from earthling.handler.dao.GoogleDAO import GoogleDAO

class GoogleCrawler(BaseCrawler):
    
    def __init__(self, dao):
        super().__init__("google", GoogleBase(), dao)

    def get_data_poly(self, data_type_name):
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

    def exec_search(self, poly, data):
        create_file_name, item_count, html_status = poly.search(
                data["keyword"], 
                idx_num = str(data["task_no"]), 
                stop=data["stop"], 
                date_start=data["date_start"], 
                date_end=data["date_end"],
                out_filepath = data["out_filepath"])

        return create_file_name, item_count, html_status