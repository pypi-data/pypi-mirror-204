import hashlib
import zipfile
from pathlib import Path
from typing import Dict, Union
from urllib import request

from tqdm import tqdm


# from https://stackoverflow.com/a/53877507
class DownloadProgressBar(tqdm):
    """Custom progress bar for download."""

    def update_to(
        self, b: float = 1, bsize: float = 1, tsize: Union[float, None] = None
    ) -> None:
        """Update tqdm progress bar.

        Parameters
        ----------
        b : float, optional
            Number of blocks transferred so far, by default 1
        bsize : float, optional
            Size of each block (in tqdm units), by default 1
        tsize : Union[float, None], optional
            Total size (in tqdm units), by default None
        """
        if tsize is not None:
            self.total = tsize
            self.update(b * bsize - self.n)


class PortfolioEntry:
    """Base class for portfolio entries.

    Attributes
    ----------
        name (str): Name of the dataset.
        url (str): URL of the dataset.
        description (str): Description of the dataset.
        license (str): License of the dataset.
        citation (str): Citation to use when referring to the dataset.
        file_name (str): Name of the downloaded file.
        md5_hash (str): MD5 hash of the downloaded file.
        files (dict[str, list]): Dictionary of files in the dataset.
        size (int): Size of the dataset in MB.
    """

    def __init__(
        self,
        name: str,
        url: str,
        description: str,
        license: str,
        citation: str,
        file_name: str,
        md5_hash: str,
        files: Dict[str, list],
        size: float = 0,
        **kwargs: str,
    ) -> None:
        self._name = name
        self._url = url
        self._description = description
        self._license = license
        self._citation = citation
        self._file_name = file_name
        self._md5_hash = md5_hash
        self._files = files
        self._size = size

    @property
    def name(self) -> str:
        """Name of the dataset.

        Returns
        -------
        str
            Name of the dataset.
        """
        return self._name

    @property
    def url(self) -> str:
        """URL of the dataset.

        Returns
        -------
        str
            URL of the dataset.
        """
        return self._url

    @property
    def description(self) -> str:
        """Description of the dataset.

        Returns
        -------
        str
            Description of the dataset.
        """
        return self._description

    @property
    def license(self) -> str:
        """License of the dataset.

        Returns
        -------
        str
            License of the dataset.
        """
        return self._license

    @property
    def citation(self) -> str:
        """Citation to use when referring to the dataset.

        Returns
        -------
        str
            Citation to use when referring to the dataset.
        """
        return self._citation

    @property
    def file_name(self) -> str:
        """Name of the downloaded file.

        Returns
        -------
        str
            Name of the downloaded file.
        """
        return self._file_name

    @property
    def md5_hash(self) -> str:
        """MD5 hash of the downloaded file.

        Returns
        -------
        str
            MD5 hash of the downloaded file.
        """
        return self._md5_hash

    @property
    def files(self) -> Dict[str, list]:
        """Dictionary of files in the dataset.

        Returns
        -------
        dict[str, list]
            Dictionary of files in the dataset.
        """
        return self._files

    @property
    def size(self) -> float:
        """Size of the dataset in MB.

        Returns
        -------
        float
            Size of the dataset in MB.
        """
        return self._size

    def download(
        self,
        path: Union[str, Path],
        check_md5: bool = True,
    ) -> dict:
        """Download dataset in the specified path.

        Parameters
        ----------
        path : str | Path
            Path to the folder in which to download the dataset.
        check_md5 : bool, optional
            Whether to check the MD5 hash of the downloaded file, by default True.

        Returns
        -------
        dict
            Dictionary of downloaded files.

        Raises
        ------
        ValueError
            If path is not a directory.
        ValueError
            If the md5 hash of the downloaded file is different from the expected one.
        """
        # TODO refactors in smaller functions
        path = Path(path)
        if path.exists() and not path.is_dir():
            raise ValueError(f"Path {path} is not a directory.")

        if not path.exists():
            path.mkdir()

        # check if zip file exists
        file_path = Path(path, self.file_name)
        if not file_path.exists():
            print(f"Downloading {self.name} to {path} might take some time.")

            # download data
            with DownloadProgressBar(
                unit="B", unit_scale=True, miniters=1, desc=self.url.split("/")[-1]
            ) as t:
                request.urlretrieve(
                    self.url, filename=file_path, reporthook=t.update_to
                )

            print("Download finished.")

        if not file_path.exists():
            raise ValueError(f"File {file_path} does not exist. Error downloading it.")

        # check if md5 hash is correct
        if check_md5:
            print(f"Checking MD5 hash of {file_path}.")

            # compute hash
            file_hash = hashlib.md5(open(file_path, "rb").read()).hexdigest()

            # compare with expected hash
            if file_hash != self.md5_hash:
                raise ValueError(
                    f"MD5 hash of {file_path} is not correct. "
                    f"Expected {self.md5_hash}, got {file_hash}."
                )

            print("MD5 hash is correct.")

        # unzip data
        data_path = Path(path, self.file_name[:-4])
        # TODO progress bar
        if zipfile.is_zipfile(file_path):
            print(f"Unzipping {file_path} to {data_path}.")

            # unzip data
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(data_path)

            print("Unzipping finished.")

        return self.files

    def to_dict(self) -> dict:
        """Convert PortfolioEntry to a dictionnary.

        Returns
        -------
            dict: A dictionnary containing the PortfolioEntry attributes.
        """
        return {
            "name": self.name,
            "url": self.url,
            "description": self.description,
            "license": self.license,
            "citation": self.citation,
            "file_name": self.file_name,
            "md5_hash": self.md5_hash,
            "files": self.files,
            "size": self.size,
        }

    def __str__(self) -> str:
        """Convert PortfolioEntry to a string.

        Returns
        -------
        str: A string containing the PortfolioEntry attributes.
        """
        return str(self.to_dict())
