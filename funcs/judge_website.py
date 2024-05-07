import time
import os
import json
import sys
import random
import openai
import re

sys.path.append("./phishIntention")
from funcs.chatgpt import run_conversation


def retry_with_exponential_backoff(
    max_retries=3, initial_delay=1, backoff_factor=2, randomness_factor=0.1
):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retry_count = 0
            delay = initial_delay

            while retry_count < max_retries:
                try:
                    return func(*args, **kwargs)
                except openai.OpenAIError as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        raise e

                    randomness = random.uniform(-randomness_factor, randomness_factor)
                    sleep_dur = delay + randomness
                    print(
                        f"OpenAI Error: {e}. Retrying in {round(sleep_dur, 2)} seconds."
                    )
                    time.sleep(sleep_dur)
                    delay *= backoff_factor
                except Exception as e:
                    raise e

        return wrapper

    return decorator


@retry_with_exponential_backoff(max_retries=3)
def run_conversation_with_retry(system, user, model):
    return run_conversation(system, user, model)


def judge_website(content, site_visual_dict, model_name, output_path, upper_limit=1000):
    start_time = time.time()
    processed_files = 0
    if os.path.exists(output_path):
        with open(output_path, "r") as f:
            detection_results = json.load(f)
    else:
        detection_results = {}

    error = set()

    system_prompt = content["system_prompt"]

    for site_num, site_dict in site_visual_dict.items():
        user_prompt = content["user_prompt"]
        if site_num == str(upper_limit):
            print("upper limit reached")
            break
        if site_num in detection_results:
            continue
        print(f"now dealing with {site_num}")
        processed_files += 1

        url = site_dict["url"]
        # visual_data = str(site_dict["visual_data"])
        visual_data = json.dumps(site_dict["visual_data"])
        visual_data = re.sub(r"(?<=[:,])\s+", "", visual_data)

        user_prompt = (
            user_prompt + "\n" + "url:" + url + "\n" + "visualdata:" + visual_data
        )

        try:
            detection_result = run_conversation_with_retry(
                system_prompt, user_prompt, model=model_name
            )

            detection_results[site_num] = detection_result
            with open(f"{output_path}", "w") as f:
                json.dump(detection_results, f, indent=4, ensure_ascii=False)

            print(f"success: site '{site_num}' is processed")
        except Exception as e:
            print(f"Error: {e}.")
            continue
    print("############################")
    end_time = time.time()
    if error:
        print(f"error: {error}")
    else:
        print("no error")
    if processed_files == 0:
        print("no files to process")
    else:
        print(f"{(end_time - start_time)/processed_files} seconds per file")
    print(f"processed {processed_files} files")
    print("finish")
