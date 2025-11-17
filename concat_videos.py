#!/usr/bin/env python3

import os
import subprocess
import json
from datetime import timedelta
from pathlib import Path

# =========================
# Script: concat_videos.py
# =========================

INPUT_DIR = "/Users/atx0mg/Downloads/jp-video/output"
CONCAT_LIST = "/Users/atx0mg/Downloads/jp-video/output/concat_list.txt"
OUTPUT_VIDEO = "/Users/atx0mg/Downloads/jp-video/output/final_output.mp4"


def get_duration(path):
    """
    Returns duration (in seconds) of a video file using ffprobe.
    """
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        path
    ]
    out = subprocess.check_output(cmd)
    data = json.loads(out)
    return float(data["format"]["duration"])


if __name__ == "__main__":

    print("📂 Scanning directory:", INPUT_DIR)

    mp4_files = sorted([
        f for f in os.listdir(INPUT_DIR)
        if f.lower().endswith(".mp4")
    ])

    if not mp4_files:
        print("❌ No MP4 files found!")
        exit()

    print("\nDetected MP4 files:")
    for f in mp4_files:
        print(" -", f)

    print("\n⏱ Extracting durations...")

    durations = []
    for f in mp4_files:
        path = os.path.join(INPUT_DIR, f)
        dur = get_duration(path)
        durations.append((f, dur))
        print(f" {f}: {dur:.2f} sec")

    print("\n⏳ Computing cumulative offsets...")

    offsets = []
    total = 0

    for fname, dur in durations:
        offsets.append((fname, str(timedelta(seconds=int(total))).zfill(8)))
        total += dur

    print("\n📘 Timecode Offsets:")
    for fname, offset in offsets:
        print(f" {fname} → {offset}")

    print("\n📝 Generating concat_list.txt ...")

    with open(CONCAT_LIST, "w") as f:
        for fname, _ in durations:
            f.write(f"file '{fname}'\n")

    print(f"✔ concat_list written to: {CONCAT_LIST}")

    print("\n🎥 Concatenating into final_output.mp4 ...")

    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", CONCAT_LIST,
        "-c", "copy",
        OUTPUT_VIDEO
    ]

    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

    print("\n🎉 DONE! Final video saved at:", OUTPUT_VIDEO)

