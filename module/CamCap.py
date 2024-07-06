import cv2

"""
 キャプチャ開始(Close忘れ注意)
"""
def OpenCap(rtsp_addr):
    # OpenCvでRTSP経由動画
    cap = cv2.VideoCapture(rtsp_addr)
    print("*** Open Capture! ***")
    return cap

"""
 キャプチャ終了
"""
def CloseCap(cap):
    # 開いているキャプチャを閉じる
    cap.release()
    print("*** Close Capture! ***")