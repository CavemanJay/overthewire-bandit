#!/usr/bin/env python3

import bz2
import gzip
import shutil
import tarfile


def tar_decompress(filename: str, outFolder: str = "."):
    with tarfile.open(filename) as f_in:
        
        import os
        
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner) 
            
        
        safe_extract(f_in, outFolder)


def bzip2_decompress(filename: str, outname: str):
    with bz2.open(filename) as f_in:
        with open(outname, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def gzip_decompress(filename: str, outname: str):
    with gzip.open(filename) as f_in:
        with open(outname, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
