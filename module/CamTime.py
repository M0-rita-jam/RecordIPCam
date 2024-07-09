import datetime

# １ファイルあたりの録画量
record_h = 0
record_m = 15
record_s = 0

# エラー検知用の許容範囲設定
acceptable_sec_range = 30  # 30%までは許容
acceptable_sec_min   = 60  # 許容時間は最小60秒(1分) 

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

"""
 録画時間の計算
"""
def GetRecTime():
    h_sec = record_h * 60 * 60
    m_sec = record_m * 60
    total_sec = h_sec + m_sec + record_s
    return total_sec

"""
  許容時間の計算
"""
def GetAcceptableTime(time_sec):
    acceptable_sec = time_sec * (acceptable_sec_range * 0.01)
    if acceptable_sec <= acceptable_sec_min:
        acceptable_sec = acceptable_sec_min
    return acceptable_sec