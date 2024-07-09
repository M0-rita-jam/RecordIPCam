import os
import sys
import cv2
import time
import threading
import datetime

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

# エラー検知用の許容範囲設定
acceptable_sec_range = 30  # 30%までは許容
acceptable_sec_min   = 60  # 許容時間は最小60秒(1分) 

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
  許容時間の計算
"""
def GetAcceptableTime(time_sec):
    acceptable_sec = time_sec * (acceptable_sec_range * 0.01)
    if acceptable_sec <= acceptable_sec_min:
        acceptable_sec = acceptable_sec_min
    return acceptable_sec

"""
 録画機能
"""
def RecMovie(cap, movie_root_path, cam_name, time_sec, acceptabletime, fps = 15):
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
    print(f"[{cam_name}]\tAcceptable Time: {acceptabletime}s")
    
    time_start = time.time()
    print(f"[{cam_name}]\tStart Time: {datetime.datetime.fromtimestamp(time_start)}")

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

            cv2.imshow(cam_name, frame) # 読み込んだフレームの表示
            cv2.waitKey(1)
        except:
            raise ValueError("なんかエラーでた。")
    print(f"[{cam_name}]\t--- Recode Stop! ---")

    # 終了
    video.release()

    time_end = time.time()
    print(f"[{cam_name}]\tEnd Time: {datetime.datetime.fromtimestamp(time_end)}")

    # 開始時間と終了時間が予定と異なる場合はエラー
    time_interval = time_end - time_start
    if time_interval > (time_sec + acceptabletime) or time_interval < (time_sec - acceptabletime):
        print(f"[{cam_name}]\t Intarval Error")
        raise ValueError("なんかエラーでた。")
    
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
def CamThreadFunc(camname ,addr ,rectime, acceptabletime):
    global g_thread_running

    cap = CamCap.OpenCap(addr)
    rec_runing = True
    while rec_runing:
        try:
            rec_runing = RecMovie(cap, "movie", camname, rectime, acceptabletime)
        except:
            # 雑すぎるエラー処理(カメラを閉じて開き直す)
            if g_thread_running == True:
                print(f"[{camname}]\t Error Catch")
                CamCap.CloseCap(cap)
                time.sleep(5)  # 特に意味はないが、すぐにやってもエラーになる気がするので5秒だけ待つ

                cap = CamCap.OpenCap(addr)
                rec_runing = True
            else:
                rec_runing = False
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
        cv2.destroyAllWindows()

"""
  動画録画(Ctrl+Cで終了)
"""
if __name__ == '__main__':
    rectime = GetRecTime()
    acceptabletime = GetAcceptableTime(rectime)
    addrs = CreateRTSPADDR_FromJson('./IPCAM_USER.json')

    cam_threads = []
    cam_maxnum = len(addrs)

    # カメラ数分のスレッド起動
    for i in range(cam_maxnum):
        cam_threads.append(threading.Thread(target=CamThreadFunc, args=(addrs[i]["cam_name"], addrs[i]["rtsp_addr"], rectime, acceptabletime)))
        cam_threads[i].start()

    # スレッド停止用の処理で待機
    CamTreadClose()