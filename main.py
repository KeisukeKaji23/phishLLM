import json

from funcs.judge_website import judge_website

from funcs.retreat_visual_data import retreat_visual_data

# 視覚情報の収集．データセットが追加されたら実行する
# phishing用
# retreat_visual_data(
#     "/home/keisukekaji/my-study/dataset/phishing/screenshots",
#     "/home/keisukekaji/my-study/dataset/phishing/site_visual_dict.json",
# )
# benign用
retreat_visual_data(
    "/home/keisukekaji/my-study/dataset/benign/screenshots",
    "/home/keisukekaji/my-study/dataset/benign/site_visual_dict.json",
)


def main(role, website_type, upper_limit):
    with open("contet.json", "r") as f:
        json_conetnt = json.load(f)
        content = json_conetnt[role]
        with open(
            f"/home/keisukekaji/my-study/dataset/{website_type}/site_visual_dict.json",
            "r",
        ) as f:
            site_visual_dict = json.load(f)
            model_name = "gpt-4-turbo"
            judge_website(
                content,
                site_visual_dict,
                model_name,
                f"/home/keisukekaji/my-study/result/{website_type}/{role}_{website_type}_result.json",
                upper_limit,
            )


main("expert", "phishing", 500)
# main("expert", "benign", 500)
main("common_person", "phishing", 500)
# main("common_person", "benign", 500)
main("common_person_with_knowledge", "phishing", 500)
# main("common_person_with_knowledge", "benign", 500)
