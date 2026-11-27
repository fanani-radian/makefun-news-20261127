#!/usr/bin/env python3
"""news-image-20261127 entry point.

Copies the bundled entry.png to $MAKEFUN_OUTPUT_DIR (default /output)
and verifies the copy byte-for-byte. If entry.png is missing, it tries a
redraw via draw.py — but that path is fully guarded: a missing PIL or
missing fonts must never break the copy path (the grader image has no
PIL, so the copy must succeed on stdlib alone).
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY = os.path.join(HERE, "entry.png")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")

    if not os.path.exists(ENTRY):
        # Redraw only when the bundled image is missing. Guarded so that
        # a missing PIL / fonts can never raise out of here.
        try:
            import subprocess
            r = subprocess.run(
                [sys.executable, os.path.join(HERE, "draw.py"), ENTRY],
                capture_output=True, timeout=120)
            if r.returncode != 0 or not os.path.exists(ENTRY):
                print("redraw failed; no entry.png available",
                      file=sys.stderr)
                return 1
        except Exception as exc:  # noqa: BLE001 - redraw is best-effort
            print("redraw unavailable (%s); no entry.png available" % exc,
                  file=sys.stderr)
            return 1

    shutil.copyfile(ENTRY, dest)
    src_size = os.path.getsize(ENTRY)
    dst_size = os.path.getsize(dest)
    if src_size != dst_size:
        print("size mismatch after copy: %d != %d" % (src_size, dst_size),
              file=sys.stderr)
        return 1
    if sha256(ENTRY) != sha256(dest):
        print("hash mismatch after copy", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, sha256 %s)" % (dest, dst_size, sha256(dest)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
