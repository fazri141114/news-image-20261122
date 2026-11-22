#!/usr/bin/env python3
"""Entrypoint for the make.fun bounty "Sum up 22 November's world news
in one image" (news-image-20261122).

The entry image ships in this repository as entry.png — THE WORLD IN
ONE DAY, an illustrated one-page summary of Sunday 22 November 2026
drawn by build_image_22.py. This program checks the file against the
bounty's limits and copies it, byte for byte, to the output path the
runner reads:

    python3 main.py [output-dir]        (default output-dir: /output)

Standard library only, no network. The copy is a pure function of the
shipped file, so two runs write identical bytes.
"""

import hashlib
import os
import struct
import sys

LIMIT_BYTES = 1_048_576  # 1 MiB
LIMIT_SIDE = 1024        # pixels per side
SIGNATURE = b"\x89PNG\r\n\x1a\n"


def read_and_check(path):
    """Return entry.png's bytes after checking the bounty's limits."""
    with open(path, "rb") as fh:
        data = fh.read()
    if len(data) > LIMIT_BYTES:
        raise ValueError(f"entry.png is {len(data)} bytes, over the 1 MiB limit")
    if data[:8] != SIGNATURE or data[12:16] != b"IHDR":
        raise ValueError("entry.png is not a whole PNG file")
    width, height = struct.unpack(">II", data[16:24])
    if width > LIMIT_SIDE or height > LIMIT_SIDE:
        raise ValueError(f"entry.png is {width}x{height}, over the 1024x1024 limit")
    return data


def main(argv):
    root = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(root, "entry.png")
    out_dir = argv[1] if len(argv) > 1 else "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    if os.path.abspath(source) == os.path.abspath(target):
        raise ValueError("output path would overwrite the shipped entry.png")

    data = read_and_check(source)
    width, height = struct.unpack(">II", data[16:24])
    with open(target, "wb") as fh:
        fh.write(data)

    digest = hashlib.sha256(data).hexdigest()
    with open(target, "rb") as fh:
        if hashlib.sha256(fh.read()).hexdigest() != digest:
            raise IOError("copied entry.png differs from the source")
    print(f"entry.png checked and copied to {target} "
          f"({width}x{height}, {len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
