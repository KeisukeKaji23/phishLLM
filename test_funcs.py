import os
import sys
sys.path.append('./phishIntention')

from funcs.image2info import image2info
from funcs.chatgpt import run_conversation
from funcs.segmentation import PhishIntentionWrapper

piw = PhishIntentionWrapper()

img_path = "/home/keisukekaji/my-study/dataset/phishing/screenshots/0/screenshot.png"
url = "/home/keisukekaji/my-study/dataset/phishing/screenshots/0/url.txt"

pred_boxes, pred_classes = piw.segmentation(img_path)
visual_data = image2info(pred_classes, pred_boxes, img_path)

print(visual_data)

order = f"""
We require a security assessment for a website. Based on the information provided below, please determine if the site is a phishing site or a legitimate, trusted site, and provide the result in a dictionary format with the keys isPhishing and reason.

URL: The URL of the site will be provided.
Visual Information: Screenshots of the webpage are divided into regions. Each region is accompanied by the following details:
Position Information: Coordinates of the region on the screen.
Text Information: Text data extracted from that specific region.
Please analyze these details and return a dictionary with:

isPhishing: A boolean value (Yes if it's a phishing site, No if it's legitimate).
reason: A brief explanation of the analysis that led to the conclusion.
"""
prompt = "order" + order  + "url" + url + "visualdata" + str(visual_data)
result = run_conversation(prompt)
print(type(result))
print(result)