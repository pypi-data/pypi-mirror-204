import hashlib

import pytest
from microscopy_portfolio import Portfolio
from microscopy_portfolio.portfolio_entry import PortfolioEntry


class FaultyMD5(PortfolioEntry):
    """Faulty PortfolioEntry.

    A PortfolioEntry with a faulty md5 hash.

    Attributes
    ----------
    name (str): Name of the dataset.
    url (str): URL to the dataset.
    file_name (str): Name of the file.
    md5_hash (str): Faulty MD5 hash.
    description (str): Description of the dataset.
    citation (str): Citation of the dataset.
    license (str): License of the dataset.
    files (dict): Dictionary of files.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Wikipedia logo",
            url="https://en.wikipedia.org/wiki/Wikipedia_logo#/media/File:Wikipedia-logo-v2.svg",
            file_name="Wikipedia-logo-v2.svg",
            md5_hash=hashlib.md5(b"I would prefer not to").hexdigest(),
            description="Wikipedia logo",
            citation="Wikipedia",
            license="CC BY-SA 3.0",
            files={
                ".": ["Wikipedia-logo-v2.svg"],
            },
            size=0.4,
        )


class PaleBlueDot(PortfolioEntry):
    """The original Pale Blue Dot image.

    Attributes
    ----------
    name (str): Name of the dataset.
    url (str): URL to the dataset.
    file_name (str): Name of the file.
    md5_hash (str): MD5 hash of the file.
    description (str): Description of the dataset.
    citation (str): Citation of the dataset.
    license (str): License of the dataset.
    files (dict): Dictionary of files.
    size (float): Size of the dataset in MB.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Wikipedia logo",
            url="https://solarsystem.nasa.gov/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBaUZoIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--4b5b6d8ce74a6930534a08e4d7dd002f24f1efcb/P36254.jpg",
            file_name="P36254.jpg",
            md5_hash="42be58bb07b17df966f6ebc41941bac7",
            description="Pale Blue Dot, credit NASA/JPL-Caltech.",
            citation="NASA/JPL-Caltech",
            license="Unknown",
            files={
                ".": ["P36254.jpg"],
            },
            size=0.4,
        )


@pytest.fixture
def faulty_portfolio_entry() -> FaultyMD5:
    """Fixture for a faulty PortfolioEntry.

    Returns
    -------
    FaultyMD5
        A PortfolioEntry with a faulty md5 hash."""
    return FaultyMD5()


@pytest.fixture
def pale_blue_dot() -> PaleBlueDot:
    """Fixture for the PaleBlueDot.

    Returns
    -------
    PaleBlueDot
        The PaleBlueDot picture.
    """
    return PaleBlueDot()


@pytest.fixture
def portfolio() -> Portfolio:
    """Fixture for the Portfolio.

    Returns
    -------
    Portfolio
        The Portfolio.
    """
    return Portfolio()
