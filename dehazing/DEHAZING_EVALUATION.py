"""Evaluate dehazed videos in dehazing/out/ against their hazy input frames in dehazing/data/.

Each video in out/ is named <method>_<source>.mp4 and is compared, frame by frame,
with the input frames of data/<source>/.

Usage:
    python DEHAZING_EVALUATION.py
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
OUT = HERE / "out"


def main() -> None:
    videos = sorted(OUT.glob("*.mp4"))
    print(f"{len(videos)} dehazed video(s) in {OUT}:")
    for v in videos:
        print(f"  {v.name}")
    raise NotImplementedError("dehazing evaluation not implemented yet")


if __name__ == "__main__":
    main()
