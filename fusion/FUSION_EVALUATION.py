"""Evaluate fused videos in fusion/out/ against their source frames in fusion/data/.

Each video in out/ is named <method>_<source>.mp4 and is compared, frame by frame,
with the visible (rgb/) and thermal (ir/) frames of data/<source>/.

For now evaluation always uses the car videos: only out/*_car_008.mp4 are considered.

Usage:
    python FUSION_EVALUATION.py
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
OUT = HERE / "out"

SOURCE = "car_008"


def main() -> None:
    videos = sorted(OUT.glob(f"*_{SOURCE}.mp4"))
    print(f"{len(videos)} fused video(s) for {SOURCE} in {OUT}:")
    for v in videos:
        print(f"  {v.name}")
    raise NotImplementedError("fusion evaluation not implemented yet")


if __name__ == "__main__":
    main()
