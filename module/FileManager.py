import os

"""
 ディレクトリの作成
"""
def Mkdir(dirpath, filepath):
    # フォルダの存在確認
    if os.path.isdir(dirpath):
        # フォルダはあった場合は特になし
        pass
    else:
        # フォルダがない場合
        if os.path.exists(filepath):
            # 同名でファイル名を作られていた場合
            pass
        else:
            # フォルダもファイルもない場合
            os.mkdir(dirpath)