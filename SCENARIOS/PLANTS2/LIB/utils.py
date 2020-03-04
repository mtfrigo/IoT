import time

from datetime import datetime, timezone

def getNowTime():
    
    return datetime.now().strftime('%d.%m %H:%M:%S')

def createNewId():
    return "id_%s" % (datetime.utcnow().strftime('%H_%M_%S'))

