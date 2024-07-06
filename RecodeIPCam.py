import os
import sys
import cv2

# スクリプトのディレクトリパスをsys.pathに追加
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# 自作moduleのimport
from module import CamTime
from module import CamCap
from module import FileManager

# １ファイルあたりの録画量
recode_h = 1
recode_m = 0
recode_s = 0

# ユーザー情報(後で書く)
user_id     = ""
user_pw     = ""
host        = ""
rtsp_addr   = f"rtsp://{user_id}:{user_pw}@{host}/stream1"

"""
 録画時間の計算
"""
def GetRecTime():
    h_sec = recode_h * 60 * 60
    m_sec = recode_m * 60
    total_sec = h_sec + m_sec + recode_s
    return total_sec

"""
 録画機能
"""
def RecMovie(cap, movie_root_path, time_sec, fps = 15):
    ret = True
    date_str = CamTime.GetDate()
    time_str = CamTime.GetTime()

    dirpath = movie_root_path + '/' + date_str
    filepath = dirpath + '/' + date_str + '_' + time_str + '.mp4'

    FileManager.Mkdir(dirpath, filepath)

    # 動画保存時の形式を設定
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    # カメラの幅を取得
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # カメラの高さを取得
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    #　情報の表示
    print(f"FilePath:{filepath}")
    print(f"Width:{w}, Height:{h}, FPS:{fps}")
    print(f"Recode Time: {time_sec}s")

    # (保存名前、fourcc,fps,サイズ)
    video = cv2.VideoWriter(filepath, fourcc, fps, (w,h))

    #　動画の保存
    print("--- Recode Start! ---")
    roop = int(fps * time_sec)
    for i in range(roop):
        try:
            cap_ret, frame = cap.read() # 1フレーム読み込み
            video.write(frame)          # 1フレーム保存する
        except KeyboardInterrupt:
            # Press '[ctrl] + [c]'
            ret = False
            break
    print("--- Recode Stop! ---")

    # 終了
    video.release()

    return ret

"""
  動画録画(Ctrl+Cで終了)
"""
if __name__ == '__main__':
    rectime = GetRecTime()
    cap = CamCap.OpenCap()
    while True:
        ret = RecMovie(cap, "movie", rectime)
        if ret == False:
            break
    CamCap.CloseCap(cap)