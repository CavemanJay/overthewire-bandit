#!/usr/bin/env python3

import bz2
import gzip
import shutil
import tarfile


def tar_decompress(filename: str, outFolder: str = "."):
    with tarfile.open(filename) as f_in:
        f_in.extractall(outFolder)


def bzip2_decompress(filename: str, outname: str):
    with bz2.open(filename) as f_in:
        with open(outname, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def gzip_decompress(filename: str, outname: str):
    with gzip.open(filename) as f_in:
        with open(outname, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
