"""Download and examine a dataset.

This script can be used to assert md5 and file size the first time
a dataset is added.
"""

import hashlib
import os
from pathlib import Path

from microscopy_portfolio import Portfolio

if __name__ == "__main__":
    # Create a portfolio object
    portfolio = Portfolio()

    # Download dataset
    root = Path("data")
    portfolio.denoising.Convallaria.download(root, check_md5=False)

    # Compute hash and size of downloaded file
    file_path = root / portfolio.denoising.Convallaria.file_name
    md5_hash = hashlib.md5(open(file_path, "rb").read()).hexdigest()
    size = os.path.getsize(file_path) / 1e6

    # Print results
    print(f"File: {file_path}")
    print(f"MD5 hash: {md5_hash}")
    print(f"Size: {size:.1f} MB")
