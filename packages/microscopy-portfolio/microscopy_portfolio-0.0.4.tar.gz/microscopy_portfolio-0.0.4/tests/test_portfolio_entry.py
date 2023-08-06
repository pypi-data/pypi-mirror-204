import pytest
from microscopy_portfolio.portfolio_entry import PortfolioEntry


def test_download(tmp_path, pale_blue_dot: PortfolioEntry):
    pale_blue_dot.download(tmp_path)


def test_download_in_invalid_path(tmp_path, pale_blue_dot: PortfolioEntry):
    """Test that downloading to an invalid path raises an error."""
    file_name = "file.txt"
    with open(tmp_path / file_name, "w") as f:
        f.write("CATS ARE NICE.")

    with pytest.raises(ValueError):
        pale_blue_dot.download(tmp_path / file_name)


def test_faulty_md5(tmp_path, faulty_portfolio_entry: PortfolioEntry):
    """Test that faulty md5 hash raises an error.

    Parameters
    ----------
        tmp_path (Path): Path to temporary directory.
        faulty_portfolio_entry (FaultyMD5): test PortfolioEntry
    """

    # test that it downloads fine when not checking md5 hash
    faulty_portfolio_entry.download(tmp_path, check_md5=False)
    assert (tmp_path / faulty_portfolio_entry.file_name).exists()

    with pytest.raises(ValueError):
        faulty_portfolio_entry.download(tmp_path, check_md5=True)


def test_change_entry(faulty_portfolio_entry):
    """Check that changing a PortfolioEntry member raises an error.

    Parameters
    ----------
    faulty_portfolio_entry : FaultyMD5
        Test PortfolioEntry.
    """
    # Verify that we can access the members
    faulty_portfolio_entry.name
    faulty_portfolio_entry.url
    faulty_portfolio_entry.description
    faulty_portfolio_entry.license
    faulty_portfolio_entry.citation
    faulty_portfolio_entry.file_name
    faulty_portfolio_entry.md5_hash
    faulty_portfolio_entry.files

    # Check that changing members raises errors
    with pytest.raises(AttributeError):
        faulty_portfolio_entry.name = ""

    with pytest.raises(AttributeError):
        faulty_portfolio_entry.url = ""

    with pytest.raises(AttributeError):
        faulty_portfolio_entry.description = ""

    with pytest.raises(AttributeError):
        faulty_portfolio_entry.license = ""

    with pytest.raises(AttributeError):
        faulty_portfolio_entry.citation = ""

    with pytest.raises(AttributeError):
        faulty_portfolio_entry.file_name = ""

    with pytest.raises(AttributeError):
        faulty_portfolio_entry.md5_hash = ""

    with pytest.raises(AttributeError):
        faulty_portfolio_entry.files = {}
