# from application.google.GoogleNews import GoogleNews
# from application.google.GoogleWeb import GoogleWeb
# from application.google.GoogleFacebook import GoogleFacebook
from earthling.handler.earthling_db_pool import exec
from connector.MySQLPoolConnector import MySQLPoolConnector, execute

print("sdfasdasd")
if __name__ == "__main__":

    f = open("test.txt", 'r')
    lines = f.readlines()
    for line in lines:
        if not line: break
        line = line.replace('\n', '')
        query = f"SELECT * FROM change_keyword_user WHERE user_id = 'jasonan8811' AND (keyword = '{line}' OR change_keyword = '{line}');"
        exec(query)
        break
        # print(query)

    f.close()


    # b = GoogleFacebook()
    # b.search(
    #     '인터넷밈', 
    #     359148, 
    #     date_start   = '2022-09-01', 
    #     date_end     = '2022-09-30',
    #     out_filepath = "test.txt")

# import json


# d = {
#     'a': "xyz",
#     'b': "poiu",
#     'c': "bvmd"
# }



# r = json.dumps(d)
# print(r)

# r = json.loads(r)
# print(type(r))

# # print(type(r))