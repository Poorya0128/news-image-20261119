"""Deliver the entry image to the output directory.

Takes entry.png, which lives next to this file, and copies it
byte-for-byte into the output folder. The folder comes from the
MAKEFUN_OUTPUT_DIR environment variable and defaults to /output
when that variable is not set. Standard library only; no network.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    source = os.path.join(HERE, "entry.png")
    target = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(source, target)


if __name__ == "__main__":
    main()
