import time
from datetime import datetime
import argparse
import os
import torch
import cv2
from phishIntention.configs import load_config
from phishIntention.modules.awl_detector import pred_rcnn, vis, find_element_type
from phishIntention.modules.logo_matching import check_domain_brand_inconsistency
from phishIntention.modules.crp_classifier import credential_classifier_mixed, html_heuristic
from phishIntention.modules.crp_locator import crp_locator
from phishIntention.utils.web_utils import driver_loader
from tqdm import tqdm
import re

os.environ['KMP_DUPLICATE_LIB_OK']='True'

class PhishIntentionWrapper:
    _caller_prefix = "PhishIntentionWrapper"
    _DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

    def __init__(self):
        self._load_config()

    def _load_config(self):
        self.AWL_MODEL, self.CRP_CLASSIFIER, self.CRP_LOCATOR_MODEL, self.SIAMESE_MODEL, self.OCR_MODEL, \
            self.SIAMESE_THRE, self.LOGO_FEATS, self.LOGO_FILES, self.DOMAIN_MAP_PATH = load_config()
        print(f'Length of reference list = {len(self.LOGO_FEATS)}')

    '''PhishIntention'''
    def segmentation(self, screenshot_path):

        waive_crp_classifier = False
        phish_category = 0  # 0 for benign, 1 for phish, default is benign
        pred_target = None
        matched_domain = None
        siamese_conf = None
        awl_detect_time = 0
        logo_match_time = 0
        crp_class_time = 0
        crp_locator_time = 0
        print("Entering PhishIntention")


        ####################### Step1: Layout detector ##############################################
        start_time = time.time()
        pred_boxes, pred_classes, _ = pred_rcnn(im=screenshot_path, predictor=self.AWL_MODEL)
        awl_detect_time += time.time() - start_time
        pred_boxes = pred_boxes.tolist()
        pred_classes = pred_classes.tolist()
        return pred_boxes, pred_classes