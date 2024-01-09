def get_crawler(channel):
    crawler = None
    if channel == "naver":
        from application.NaverCrawler import NaverCrawler
        crawler = NaverCrawler()
    
    elif channel == "google":
        from application.GoogleCrawler import GoogleCrawler
        crawler = GoogleCrawler()
    
    elif channel == "daum":
        from application.DaumCrawler import DaumCrawler
        crawler = DaumCrawler()
    return crawler

