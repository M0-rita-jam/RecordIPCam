import json

"""
 Jsonファイルの読み込み
"""
def OpenJson(filepath):
    json_file = open(filepath, 'r')
    json_dict = json.load(json_file)
    return json_dict

"""
 RTSPのアドレスをParse
"""
def ParseRTSP_FromJson(cam_dict):
    user_id = cam_dict['user_id']
    user_pw = cam_dict['user_pw']
    host_ip = cam_dict['host_ip']
    rtsp_addr   = f"rtsp://{user_id}:{user_pw}@{host_ip}/stream1"

    return {"cam_name":cam_dict["cam_name"], "rtsp_addr":rtsp_addr}