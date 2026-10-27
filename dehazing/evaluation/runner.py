from pathlib import Path

import pandas as pd

from .datasets import pair_folders, read_image
from .metrics import FULL_REF, HAZY_REF, NO_REF

#score each method outputs and the hazy input as baseline 
def evaluate(data_root, methods, n=None):
    """
    data_root : folder with hazy/ and GT/
    methods   : {"label": folder of dehazed outputs}
    n         : only use the first n images
    returns (per_image, summary): one row per (image, method), and the mean per method
    """
    root = Path(data_root)
    labels = ["hazy"] + list(methods)
    pairs = pair_folders(root / "hazy", root / "GT", *methods.values())[:n]

    rows = []
    for i, (hazy_path, gt_path, *output_paths) in enumerate(pairs):
        gt = read_image(gt_path)
        hazy = read_image(hazy_path)
        for label, path in zip(labels, [hazy_path, *output_paths]):
            img = read_image(path)
            row = {"image": hazy_path.stem, "method": label}
            row.update({name: fn(img, gt) for name, fn in FULL_REF.items()})
            row.update({name: fn(img) for name, fn in NO_REF.items()})
            row.update({name: fn(img, hazy) for name, fn in HAZY_REF.items()})
            rows.append(row)
        print(f"[{i + 1}/{len(pairs)}] {hazy_path.name}")

    per_image = pd.DataFrame(rows)
    summary = per_image.groupby("method", sort=False).mean(numeric_only=True)
    return per_image, summary