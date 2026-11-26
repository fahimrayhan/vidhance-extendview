"""Example frames for RFN-Nest Blender v1, v2, v3, v3+CLAHE, v3+DCP on the three forest test clips.

Writes out/examples/<source>.png: one grid per clip (hazy input | thermal | fog-free reference on top,
then the published RFN-Nest and the five variants), same frame everywhere, labelled with SSIM_ref / PSNR_ref
from fusion_results.csv. Run from fusion/: python make_examples.py
"""
from pathlib import Path
import cv2, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
SOURCES = ["forest_01_night-moon_nadir-hover", "forest_07_afternoon_steep-push", "forest_10_dusk_high-orbit"]
METHODS = [("rfn_nest", "RFN-Nest (published)"), ("rfn_nest_blender", "v1"), ("rfn_nest_blender_v2", "v2"),
           ("rfn_nest_blender_v3", "v3"), ("rfn_nest_blender_v3+clahe", "v3 + CLAHE"),
           ("rfn_nest_blender_v3+dcp", "v3 + DCP")]
res = pd.read_csv(HERE / "fusion_results.csv").set_index(["method", "source"])
out_dir = HERE / "out" / "examples"
out_dir.mkdir(parents=True, exist_ok=True)


def video_frame(path, i):
    cap = cv2.VideoCapture(str(path))
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ok, f = cap.read()
    cap.release()
    if not ok:
        raise RuntimeError(f"cannot read frame {i} of {path}")
    return cv2.cvtColor(f, cv2.COLOR_BGR2RGB)


def image(path):
    return cv2.cvtColor(cv2.imread(str(path)), cv2.COLOR_BGR2RGB)


for src in SOURCES:
    d = HERE / "data" / src
    names = sorted(p.name for p in (d / "rgb").iterdir())
    i = len(names) // 2
    r = res.loc[("rfn_nest", src)]
    panels = [(image(d / "rgb" / names[i]), f"hazy visible input\nSSIM_ref {r.SSIM_ref_vis:.3f} · PSNR_ref {r.PSNR_ref_vis:.2f}"),
              (image(d / "ir" / names[i]), "thermal input"),
              (image(d / "clear" / names[i]), "fog-free reference")]
    for m, label in METHODS:
        r = res.loc[(m, src)]
        panels.append((video_frame(HERE / "out" / f"{m}_{src}.mp4", i),
                       f"{label}\nSSIM_ref {r.SSIM_ref:.3f} · PSNR_ref {r.PSNR_ref:.2f} · N^AB/F {r.Nabf:.2f}"))
    h, w = panels[0][0].shape[:2]
    fig, axes = plt.subplots(3, 3, figsize=(18, 18 * h / w + 1.6))
    for ax, (img, title) in zip(axes.flat, panels):
        ax.imshow(img)
        ax.set_title(title, fontsize=12)
        ax.axis("off")
    fig.suptitle(f"{src}  —  frame {i + 1}/{len(names)}", fontsize=15)
    fig.tight_layout()
    fig.savefig(out_dir / f"{src}.png", dpi=110)
    plt.close(fig)
    print(out_dir / f"{src}.png")
