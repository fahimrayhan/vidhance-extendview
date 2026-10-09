from pathlib import Path

import cv2


def read_image(path):
    #read image as uint8 BGR (H, W, 3).
    return cv2.imread(str(path))


def pair_folders(*folders):
    #(hazy_1, gt_1, out_1)
    return list(zip(*[sorted(Path(f).iterdir()) for f in folders]))