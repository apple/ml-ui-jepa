#
# For licensing see accompanying LICENSE file.
# Copyright (C) 2025 Apple Inc. All Rights Reserved.
#

import argparse
import os 
from os.path import expanduser
import requests
import sys

def progress_bar(current, total, bar_length=40):
    if total==0:
        bar = '#' * bar_length
        sys.stdout.write(f'\r[{bar}] ??%')
        return

    fraction = current / total
    completed = int(bar_length * fraction)
    bar = '#' * completed + '.' * (bar_length - completed)
    percent = int(fraction * 100)
    sys.stdout.write(f'\r[{bar}] {percent}%')
    sys.stdout.flush()


def download_file(url, output_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    chunk_size = 8192

    with open(output_path, 'wb') as f:
        downloaded = 0
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                progress_bar(downloaded, total_size)
    
    print("\nDownload finished.")

parser = argparse.ArgumentParser()
parser.add_argument(
    "--type",
    type=str,
    choices=["iit", "iiw"],
    required=True,
    help="Choose a dataset from: iit, iiw"
)
parser.add_argument(
    "--output_dir",
    help="Provide an output directory"
)
args = parser.parse_args()

if not os.path.isdir(args.output_dir):
    print(f"Directory {args.output_dir} doesn't exist")
    exit(0)


if args.type=="iit":
    url = "https://ml-site.cdn-apple.com/datasets/ui-jepa/iit-1.0.0/data/raw.zip"
else:
    url = "https://ml-site.cdn-apple.com/datasets/ui-jepa/iiw-1.0.0/data/raw.zip"

clean_output_dir = os.path.abspath(os.path.normpath(expanduser(args.output_dir.strip())))
file_path = os.path.join(clean_output_dir, "raw.zip")
download_file(url=url, output_path=file_path)