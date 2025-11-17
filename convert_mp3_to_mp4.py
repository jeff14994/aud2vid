import os
import subprocess
from pathlib import Path

# =========================
# Script: convert_mp3_to_mp4.py
# =========================

INPUT_DIR = "/Users/atx0mg/Downloads/jp-video/input"
OUTPUT_DIR = "/Users/atx0mg/Downloads/jp-video/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_mp3_to_mp4(input_path, output_path):
    """
    Converts MP3 to MP4 by generating a black background video.
    Uses FFmpeg lavfi filter instead of treating color= as a file.
    """
    cmd = [
        "ffmpeg",
        "-f", "lavfi",
        "-i", "color=black:s=1920x1080",
        "-i", input_path,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        "-shortest",
        output_path
    ]

    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"✔ Converted: {input_path} → {output_path}")


# =========================
# Main execution
# =========================
if __name__ == "__main__":
    mp3_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".mp3")])

    if not mp3_files:
        print("No MP3 files found in:", INPUT_DIR)
        exit()

    print("Found MP3 files:")
    for f in mp3_files:
        print(" -", f)

    for mp3 in mp3_files:
        src = os.path.join(INPUT_DIR, mp3)
        name = Path(mp3).stem
        dest = os.path.join(OUTPUT_DIR, f"{name}.mp4")

        convert_mp3_to_mp4(src, dest)

    print("\n🎉 All conversions complete!")

