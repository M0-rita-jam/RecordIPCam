import os
import sys
import cv2
import time
import threading

# スクリプトのディレクトリパスをsys.pathに追加
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# 自作moduleのimport
from module import CamTime
from module import CamCap
from module import FileManager
from module import JsonManager

# １ファイルあたりの録画量
recode_h = 0
recode_m = 15
recode_s = 0

# スレッドが動いているかどうかのフラグ
g_thread_running = True

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
def RecMovie(cap, movie_root_path, cam_name, time_sec, fps = 15):
    global g_thread_running

    ret = True
    date_str = CamTime.GetDate()
    time_str = CamTime.GetTime()

    dirpath = movie_root_path + '/' + date_str
    filepath = dirpath + '/' + cam_name + '_' + date_str + '_' + time_str + '.mp4'

    FileManager.Mkdir(dirpath, filepath)

    # 動画保存時の形式を設定
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    # カメラの幅を取得
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # カメラの高さを取得
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    #　情報の表示
    print(f"[{cam_name}]\tFilePath:{filepath}")
    print(f"[{cam_name}]\tWidth:{w}, Height:{h}, FPS:{fps}")
    print(f"[{cam_name}]\tRecode Time: {time_sec}s")

    # (保存名前、fourcc,fps,サイズ)
    video = cv2.VideoWriter(filepath, fourcc, fps, (w,h))

    #　動画の保存
    print(f"[{cam_name}]\t--- Recode Start! ---")
    max_frame = int(fps * time_sec)
    for i in range(max_frame):
        if g_thread_running == False:
            # スレッド終了命令を受けていた場合は終了
            print(f"[{cam_name}]\t--- Thread Stop! ---")
            ret = False
            break

        try:
            cap_ret, frame = cap.read() # 1フレーム読み込み
            video.write(frame)          # 1フレーム保存する
        except:
            # [TODO] 詳しいエラー処理は後で考える
            ret = False
            break
    print(f"[{cam_name}]\t--- Recode Stop! ---")

    # 終了
    video.release()

    return ret

"""
  JsonからRTSPのアドレスを作成
"""
def CreateRTSPADDR_FromJson(filepath):
    userdata = JsonManager.OpenJson(filepath)
    rtsp_addr = []
    for camdata in userdata["cams"]:
        rtsp_addr.append(JsonManager.ParseRTSP_FromJson(camdata))

    return rtsp_addr

"""
  実際にスレッドで動かす処理
"""
def CamThreadFunc(camname ,addr ,rectime):
    global g_thread_running

    cap = CamCap.OpenCap(addr)
    rec_runing = True
    while rec_runing:
        rec_runing = RecMovie(cap, "movie", camname, rectime)
    CamCap.CloseCap(cap)

"""
  スレッドを止める用の処理
"""
def CamTreadClose():
    global g_thread_running

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Press '[ctrl] + [c]'
        g_thread_running = False

"""
  動画録画(Ctrl+Cで終了)
"""
if __name__ == '__main__':
    rectime = GetRecTime()
    addrs = CreateRTSPADDR_FromJson('./IPCAM_USER.json')

    cam_threads = []
    cam_maxnum = len(addrs)

    # カメラ数分のスレッド起動
    for i in range(cam_maxnum):
        cam_threads.append(threading.Thread(target=CamThreadFunc, args=(addrs[i]["cam_name"], addrs[i]["rtsp_addr"], rectime)))
        cam_threads[i].start()

    # スレッド停止用の処理で待機
    CamTreadClose()