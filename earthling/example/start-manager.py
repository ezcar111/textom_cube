import os
from earthling_edum.service.ComManager import *

if __name__ == "__main__":

    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    
    if not os.path.isdir("./logs"):
        os.mkdir("./logs")
    run()
