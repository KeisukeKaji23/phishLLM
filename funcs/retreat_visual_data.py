import pathlib
import json
import sys
import os
import time
from natsort import natsorted

sys.path.append("./phishIntention")
from funcs.image2info import image2info
from funcs.segmentation import PhishIntentionWrapper

piw = PhishIntentionWrapper()


def retreat_visual_data(ss_dir, output_file):
    start_time = time.time()
    processed_files = 0
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            site_visual_dict = json.load(f)
    else:
        site_visual_dict = {}

    site_folders = list(pathlib.Path(ss_dir).iterdir())
    # 文字順に並び変える
    site_folders = natsorted(site_folders, key=lambda x: x.name)
    error = set()

    for site_folder in site_folders:
        folder_name = site_folder.name
        if folder_name in site_visual_dict:
            continue
        print(f"now dealing with {folder_name}")
        processed_files += 1

        # url.txtを読み取る操作
        url_path = os.path.join(site_folder, "url.txt")
        if os.path.exists(url_path):
            with open(url_path, "r") as f:
                url = f.read()
        else:
            error.add(folder_name)
            print(f"error url.txt is none: {folder_name}")
            continue

        # screenshot.pngを読み取る操作
        screenshot_path = os.path.join(site_folder, "screenshot.png")
        if os.path.exists(screenshot_path):
            pred_boxes, pred_classes = piw.segmentation(screenshot_path)
            visual_data = image2info(pred_classes, pred_boxes, screenshot_path)
            site_visual_dict[folder_name] = {
                "url": url,
                "ss_path": screenshot_path,
                "visual_data": visual_data,
            }
            with open(output_file, "w") as f:
                json.dump(site_visual_dict, f, indent=4, ensure_ascii=False)

            print(f"success: folder '{folder_name}' is processed")
        else:
            error.add(folder_name)
            print(f"error screenshot.png is none: {folder_name}")
            continue
    print("##################################################")
    end_time = time.time()
    if error:
        print(f"error: {error}")
    else:
        print("no error")
    if processed_files == 0:
        print("no files to process")
    else:
        print(f"{(end_time - start_time)/processed_files} seconds per file")
    print("finish")
