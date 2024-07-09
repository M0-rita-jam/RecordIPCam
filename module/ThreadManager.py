import cv2
import time
import threading
import datetime

# 自作moduleのimport
from module import CamTime
from module import CamCap
from module import FileManager
from module import gloval_value as g


"""
 録画機能
"""
def RecMovie(cap, movie_root_path, cam_name, time_sec, acceptabletime, fps = 15):
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
    print(f"[{cam_name}]\tRecord Time: {time_sec}s")
    print(f"[{cam_name}]\tAcceptable Time: {acceptabletime}s")
    
    time_start = time.time()
    print(f"[{cam_name}]\tStart Time   : {datetime.datetime.fromtimestamp(time_start)}")
    print(f"[{cam_name}]\tSchedule Time: {datetime.datetime.fromtimestamp(time_start + time_sec)}")

    # (保存名前、fourcc,fps,サイズ)
    video = cv2.VideoWriter(filepath, fourcc, fps, (w,h))

    #　動画の保存
    print(f"[{cam_name}]\t--- Record Start! ---")
    max_frame = int(fps * time_sec)
    time_prev = time.time()
    for i in range(max_frame):
        time_now = time.time()
        if time_now > (time_start + time_sec + acceptabletime):
            print(f"[{cam_name}]\t Recording time exceeded.")
            break

        if (time_prev - time_now) > 1:
            print(f"[{cam_name}]\t Camera timeout occurred.")
            break

        if g.thread_running == False:
            # スレッド終了命令を受けていた場合は終了
            print(f"[{cam_name}]\t--- Thread Stop! ---")
            ret = False
            break

        try:
            cap_ret, frame = cap.read() # 1フレーム読み込み
            video.write(frame)          # 1フレーム保存する
        except:
            print(f"[{cam_name}]\t フレーム読み込み失敗")
            break
        time_prev = time.time()
    print(f"[{cam_name}]\t--- Record Stop! ---")

    # 終了
    video.release()

    time_end = time.time()
    print(f"[{cam_name}]\tEnd Time: {datetime.datetime.fromtimestamp(time_end)}")

    # 開始時間と終了時間が予定と異なる場合はエラー
    time_interval = time_end - time_start
    if time_interval > (time_sec + acceptabletime) or time_interval < (time_sec - acceptabletime):
        raise ValueError(f"[{cam_name}]\t Intarval Error")
    
    return ret

"""
  実際にスレッドで動かす処理
"""
def CamThreadFunc(camname, addr ,rectime, acceptabletime):
    cap = CamCap.OpenCap(camname, addr)
    rec_runing = True
    while rec_runing:
        try:
            rec_runing = RecMovie(cap, "movie", camname, rectime, acceptabletime)
        except Exception as e:
            # 雑すぎるエラー処理(カメラを閉じて開き直す)
            if g.thread_running == True:
                print(f"{e}")
                cap = CamCap.ReOpenCap(camname, cap, addr)
                rec_runing = True
            else:
                rec_runing = False
    CamCap.CloseCap(camname, cap)

"""
  カメラスレッドの作成
"""
def CamThreadCreate(camname ,addr ,rectime, acceptabletime):
    return threading.Thread(target=CamThreadFunc, args=(camname ,addr, rectime, acceptabletime))

"""
  スレッドを止める用の処理
"""
def CamTreadClose():
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Press '[ctrl] + [c]'
        g.thread_running = False
        cv2.destroyAllWindows()