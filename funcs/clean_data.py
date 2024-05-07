import json
import os
from collections import OrderedDict


def clean_data(target_path):
    # JSONファイルを読み込む
    with open(target_path, "r") as f:
        data = json.load(f)

    # キーを整数に変換して並べ替える
    sorted_data = OrderedDict(sorted(data.items(), key=lambda x: int(x[0])))

    # 並べ替えたデータを新しいJSONファイルに書き込む
    with open(target_path, "w") as f:
        json.dump(sorted_data, f, indent=4)

    print("Data cleaning is done!")


# clean_data("/home/keisukekaji/my-study/dataset/phishing/site_visual_dict.json")
# clean_data("/home/keisukekaji/my-study/dataset/benign/site_visual_dict.json")
