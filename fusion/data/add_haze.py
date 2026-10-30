from pathlib import Path
import shutil, cv2, numpy as np
import os

DATA = Path("fusion/data")
SOURCE = "car_008"
T = 0.5      # transmission: 0.8 light, 0.5 moderate, 0.3 dense
A = 0.9      # airlight brightness
DST_NAME = f"{SOURCE}_haze_{int(T * 100)}"

def add_haze(bgr, t=T, a=A):
    x = bgr.astype(np.float32) / 255.0
    return (np.clip(x * t + a * (1 - t), 0, 1) * 255 + 0.5).astype(np.uint8)

src, dst = DATA / SOURCE, DATA / DST_NAME
dst.mkdir(exist_ok=True)

# copy everything except the visible stream (ir/, thermal.mp4, rgb.txt, ir.txt, ...)
for p in src.iterdir():
    if p.name in ("rgb", "visible.mp4"):
        continue
    if p.is_dir():
        shutil.copytree(p, dst / p.name, dirs_exist_ok=True)
    else:
        shutil.copy2(p, dst / p.name)

if (src / "rgb").is_dir():                               # image sequence
    (dst / "rgb").mkdir(exist_ok=True)
    for f in sorted((src / "rgb").iterdir()):
        if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"}:
            cv2.imwrite(str(dst / "rgb" / f.name), add_haze(cv2.imread(str(f))),
                        [cv2.IMWRITE_JPEG_QUALITY, 95])
else:                                                    # visible.mp4
    cap = cv2.VideoCapture(str(src / "visible.mp4"))
    w, h = int(cap.get(3)), int(cap.get(4))
    out = cv2.VideoWriter(str(dst / "visible.mp4"), cv2.VideoWriter_fourcc(*"mp4v"), cap.get(5), (w, h))
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        out.write(add_haze(frame))
    cap.release(); out.release()

print("wrote", dst)