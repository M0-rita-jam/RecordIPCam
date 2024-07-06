import json

"""
 Jsonファイルの読み込み
"""
def OpenJson(filepath):
    json_file = open(filepath, 'r')
    json_dict = json.load(json_file)
    return json_dict
    