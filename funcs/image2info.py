import json
import time
import numpy as np
from PIL import Image
from .googleVision import detect_logos, detect_text


def image2info(pred_classes, pred_boxes, img_path, output_json=False):
    # Initialize a dictionary to store the results
    results = {}
    # Open the screenshot with PIL
    img = Image.open(img_path)
    # Process each segment
    for i in range(len(pred_classes)):
        # Get the class and bounding box of the current segment
        pred_class = pred_classes[i]
        pred_box = pred_boxes[i]  # Convert to int for PIL

        # Crop the current segment from the screenshot
        segment = img.crop(pred_box)

        # Initialize a dictionary to store the results for the current segment
        segment_results = {"position": [int(x) for x in pred_box]}

        # Perform image recognition on the segment and store the results
        if pred_class == 0:  # logo
            logo_info = detect_logos(segment)
            segment_results["logos"] = logo_info
        else:  # input box, button, block
            text_info = detect_text(segment)
            segment_results["texts"] = text_info

        # Store the results for the current segment
        results[str(i + 1)] = [segment_results]

    if output_json:
        with open(
            "/home/keisuke/my-study/PhishIntention/results.json", "w", encoding="utf8"
        ) as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

    return results
