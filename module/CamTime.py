import datetime

"""
 YYYYMMDDの形式で現在の日時を取得
"""
def GetDate():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d')

"""
 hh:mm:ssの形式で現在の時刻を取得
"""
def GetTime():
    now = datetime.datetime.now()
    return now.strftime('%H%M%S')