import cv2
import time

"""
 キャプチャ開始(Close忘れ注意)
"""
def OpenCap(rtsp_addr):
    print("Target RTSP ADDR:{0}".format(rtsp_addr))
    # OpenCvでRTSP経由動画
    cap = cv2.VideoCapture(rtsp_addr)
    print("*** Open Capture! ***")
    return cap

"""
 キャプチャ終了(Close後に再度実行しても問題なし)
"""
def CloseCap(cap):
    # 開いているキャプチャを閉じる
    cap.release()
    print("*** Close Capture! ***")

"""
  キャプチャを開きなおす
"""
def ReOpenCap(cap, rtsp_addr):
    CloseCap(cap)
    time.sleep(5)  # 特に意味はないが、すぐにやってもエラーになる気がするので5秒だけ待つ
    cap = OpenCap(rtsp_addr)

    return cap