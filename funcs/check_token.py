import tiktoken
import json
import re

# To get the tokeniser corresponding to a specific model in the OpenAI API:
enc = tiktoken.encoding_for_model("gpt-4")

tmp = enc.encode("Hello, world!")

input_dpt = 0.01 / 1000
sum_token_input = 8400 + 13900
max_token_input = 0
max_token_idx = -1
output_dpt = 0.03 / 1000
sum_token_output = 0


def remove_whitespace(text):
    text = re.sub(r"\n", "", text)  # 改行の削除
    text = re.sub(r"\t", "", text)  # タブの削除
    return text


with open("/home/keisukekaji/my-study/dataset/benign/site_visual_dict.json", "r") as f:
    site_visual_dict = json.load(f)
    for site_num, site_dict in site_visual_dict.items():
        data = str(site_dict["visual_data"])
        data = remove_whitespace(data)
        tokens = enc.encode(data)
        sum_token_input += len(tokens)
        if len(tokens) > max_token_input:
            max_token_input = max(max_token_input, len(tokens))
            max_token_idx = site_num


with open(
    "/home/keisukekaji/my-study/result/benign/expert_benign_result.json", "r"
) as f:
    detection_results = json.load(f)
    for site_num, detection_result in detection_results.items():
        tokens = enc.encode(str(detection_result))
        sum_token_output += len(tokens)

print(input_dpt * sum_token_input + output_dpt * sum_token_output)
print(max_token_input)
print(max_token_idx)
print(sum_token_input)
print(sum_token_output)
