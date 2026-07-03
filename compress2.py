#!/usr/bin/env python3
import subprocess, os, sys

repo_dir = os.path.expanduser("~/Downloads/WerksLearning")
repo_dir = os.path.realpath(repo_dir)
SKIP = ["macOS Tahoe - Tutorial"]

def size_mb(path):
    return os.path.getsize(path) / (1024 * 1024)

total_saved = 0.0
for root, dirs, files in os.walk(repo_dir):
    dirs[:] = [d for d in dirs if d != '.git']
    for name in files:
        if not name.endswith('.mp4'):
            continue
        path = os.path.join(root, name)
        mb = size_mb(path)
        if mb < 10:
            continue
        if any(s in name for s in SKIP):
            print(f"SKIP  {mb:.0f}M  {name}")
            continue
        tmp = path + ".__tmp__.mp4"
        before = mb
        r = subprocess.run(
            ["ffmpeg", "-i", path,
             "-c:v", "libx264", "-crf", "32", "-preset", "slow",
             "-c:a", "aac", "-b:a", "96k",
             "-y", tmp],
            capture_output=True
        )
        if r.returncode == 0 and os.path.exists(tmp):
            after = size_mb(tmp)
            if after < before:
                os.replace(tmp, path)
                saved = before - after
                total_saved += saved
                print(f"✓  {before:.0f}M → {after:.0f}M  (saved {saved:.0f}M)  {name}")
            else:
                os.remove(tmp)
                print(f"SKIP (no gain)  {before:.0f}M  {name}")
        else:
            if os.path.exists(tmp):
                os.remove(tmp)
            print(f"✗ FAILED  {name}")
        sys.stdout.flush()

print(f"\nTotal saved: {total_saved:.0f} MB")
