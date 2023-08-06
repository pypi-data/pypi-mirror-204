import os
from pathlib import Path
from typing import Dict, List

import pytest
from microscopy_portfolio.portfolio import IterablePortfolio
from microscopy_portfolio.portfolio_entry import PortfolioEntry


def file_checker(path: Path, root_name: str, files: Dict[str, List[str]]) -> None:
    for folder, file_list in files.items():
        folder_path = path / root_name / folder
        for file in file_list:
            assert (
                folder_path / file
            ).is_file(), f"{file} does not exist in {folder_path}."


def unique_url_checker(iter_portfolio: IterablePortfolio) -> None:
    urls = []
    for entry in iter_portfolio:
        # add to list of urls
        urls.append(entry.url)

    assert len(urls) == len(set(urls)), f"Duplicated urls in {iter_portfolio.name}."


def unique_md5_checker(iter_portfolio: IterablePortfolio) -> None:
    hashes = []
    for entry in iter_portfolio:
        # add to list of hashes
        hashes.append(entry.md5_hash)

    assert len(hashes) == len(
        set(hashes)
    ), f"Duplicated hashes in {iter_portfolio.name}."


def portoflio_entry_checker(entry: PortfolioEntry) -> None:
    assert entry.name is not None and entry.name != "", f"Invalid name in {entry}"
    assert entry.url is not None and entry.url != "", f"Invalid url in {entry}"
    assert (
        entry.md5_hash is not None and entry.md5_hash != ""
    ), f"Invalid md5 hash in {entry}"
    assert (
        entry.description is not None and entry.description != ""
    ), f"Invalid description in {entry}"
    assert (
        entry.citation is not None and entry.citation != ""
    ), f"Invalid citation in {entry}"
    assert (
        entry.license is not None and entry.license != ""
    ), f"Invalid license in {entry}"
    assert (
        entry.file_name is not None and entry.file_name != ""
    ), f"Invalid file name in {entry}"
    assert entry.files is not None and len(entry.files) > 0, f"Invalid files in {entry}"
    assert entry.size is not None and entry.size > 0, f"Invalid size in {entry}"


def download_checker(path: Path, dataset: PortfolioEntry) -> None:
    # download dataset
    dataset.download(path, check_md5=True)

    # check that the zip file exists
    path_to_zip = path / dataset.file_name
    assert path_to_zip.exists(), f"{dataset.file_name} does not exist after download."

    # check that the files are there
    file_checker(path, dataset.file_name[:-4], dataset.files)

    # check file size with a tolerance of 5% or 3MB
    file_size = os.path.getsize(path_to_zip) / 1024 / 1024  # MB
    abs_tolerance = max(0.05 * dataset.size, 3)
    assert dataset.size == pytest.approx(file_size, abs=abs_tolerance), (
        f"{dataset.name} has not the expected size "
        f"(expected {dataset.size}, got {file_size})."
    )
