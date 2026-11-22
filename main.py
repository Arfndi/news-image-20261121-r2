#!/usr/bin/env python3
"""news-image-20261121 round 2 entrypoint (Python 3.13, stdlib only).

Copies the pre-rendered board (entry.png, drawn at build time by
render_board.py) to the grader's output directory. No network, no
image libraries, no randomness: the same bytes every run.
"""
import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    src_size = os.path.getsize(src)
    dst_size = os.path.getsize(dst)
    if src_size != dst_size:
        raise SystemExit("copy mismatch: %d bytes in, %d bytes out"
                         % (src_size, dst_size))
    if src_size > 1048576:
        raise SystemExit("entry.png is %d bytes, over the 1 MiB cap"
                         % src_size)
    print("wrote %s (%d bytes)" % (dst, dst_size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
