from enum import Enum

from .portfolio_entry import PortfolioEntry


class NoiseLevel(str, Enum):
    """An IntEnum representing the noise level of a dataset.

    N0 corresponds to the noise-free version of the dataset, N10 and N20 to
    images corrupted with Gaussian noise with zero-mean and standard deviations
    of 10 and 20, respectively.
    """

    N0 = "0"
    N10 = "10"
    N20 = "20"


class NoisyObject:
    """A mixin class for datasets with different noise levels.

    Attributes
    ----------
    noise_level (NoiseLevel): Noise level of the dataset.
    """

    def __init__(self, noise_level: NoiseLevel = NoiseLevel.N0, **kwargs: str) -> None:
        self._noise_level = noise_level

    @property
    def noise_level(self) -> NoiseLevel:
        """Noise level of the dataset."""
        return self._noise_level


class DSB2018(PortfolioEntry, NoisyObject):
    """The 2018 Data Science Bowl dataset used by DenoiSeg.

    The dataset is available in three different noise levels: N0, N10 and N20.


    Attributes
    ----------
    noise_level (NoiseLevel): Noise level of the dataset.
    """

    def __init__(self, noise_level: NoiseLevel = NoiseLevel.N0) -> None:
        """Initialize a DSB2018 instance.

        Parameters
        ----------
        noise_level : NoiseLevel, optional
            Noise level of the dataset, by default NoiseLevel.N0
        """
        super().__init__(
            noise_level=noise_level,
            name=f"DSB2018_n{noise_level.value}",
            url=self._get_url(noise_level),
            file_name=f"DSB2018_n{noise_level.value}.zip",
            md5_hash=self._get_hash(noise_level),
            description="From the Kaggle 2018 Data Science Bowl challenge, the "
            "training and validation sets consist of 3800 and 670 patches "
            "respectively, while the test set counts 50 images.\n"
            "Original data: "
            "https://www.kaggle.com/competitions/data-science-bowl-2018/data",
            license="GPL-3.0",
            citation="Caicedo, J.C., Goodman, A., Karhohs, K.W. et al. Nucleus "
            "segmentation across imaging experiments: the 2018 Data Science "
            "Bowl. Nat Methods 16, 1247-1253 (2019). "
            "https://doi.org/10.1038/s41592-019-0612-7",
            files={
                f"DSB2018_n{noise_level.value}/train": ["train_data.npz"],
                f"DSB2018_n{noise_level.value}/test": ["test_data.npz"],
            },
            size=self._get_size(noise_level),
        )

    @staticmethod
    def _get_url(noise: NoiseLevel) -> str:
        if noise == NoiseLevel.N0:
            return "https://zenodo.org/record/5156969/files/DSB2018_n0.zip?download=1"
        elif noise == NoiseLevel.N10:
            return "https://zenodo.org/record/5156977/files/DSB2018_n10.zip?download=1"
        else:
            return "https://zenodo.org/record/5156983/files/DSB2018_n20.zip?download=1"

    @staticmethod
    def _get_hash(noise: NoiseLevel) -> str:
        if noise == NoiseLevel.N0:
            return "80513b1eda8e08df1d8dcc5543ad1ad1"
        elif noise == NoiseLevel.N10:
            return "aa16c116949d8b8cd573d7bbeacbd0c3"
        else:
            return "81abc17313582a4f04f501e3dce1fe88"

    @staticmethod
    def _get_size(noise: NoiseLevel) -> float:
        if noise == NoiseLevel.N0:
            return 40.2
        elif noise == NoiseLevel.N10:
            return 366.0
        else:
            return 368.0


class SegFlywing(PortfolioEntry, NoisyObject):
    """Flywing dataset used by DenoiSeg.

    The dataset is available in three different noise levels: N0, N10 and N20.


    Attributes
    ----------
    noise_level (NoiseLevel): Noise level of the dataset.
    """

    def __init__(self, noise_level: NoiseLevel = NoiseLevel.N0) -> None:
        """Initialize a Flywing instance.

        Parameters
        ----------
        noise_level : NoiseLevel, optional
            Noise level of the dataset, by default NoiseLevel.N0
        """
        super().__init__(
            noise_level=noise_level,
            name=f"Flywing_n{noise_level.value}",
            url=self._get_url(noise_level),
            file_name=f"Flywing_n{noise_level.value}.zip",
            md5_hash=self._get_hash(noise_level),
            description="This dataset consist of 1428 training and 252 "
            "validation patches of a membrane labeled fly wing. The test set "
            "is comprised of 50 additional images.",
            license="CC BY-SA 4.0",
            citation="Buchholz, T.O., Prakash, M., Schmidt, D., Krull, A., Jug, "
            "F.: Denoiseg: joint denoising and segmentation. In: European "
            "Conference on Computer Vision (ECCV). pp. 324-337. Springer (2020) 8, 9",
            files={
                f"Flywing_n{noise_level.value}/train": ["train_data.npz"],
                f"Flywing_n{noise_level.value}/test": ["test_data.npz"],
            },
            size=self._get_size(noise_level),
        )

    @staticmethod
    def _get_url(noise: NoiseLevel) -> str:
        if noise == NoiseLevel.N0:
            return "https://zenodo.org/record/5156991/files/Flywing_n0.zip?download=1"
        elif noise == NoiseLevel.N10:
            return "https://zenodo.org/record/5156993/files/Flywing_n10.zip?download=1"
        else:
            return "https://zenodo.org/record/5156995/files/Flywing_n20.zip?download=1"

    @staticmethod
    def _get_hash(noise: NoiseLevel) -> str:
        if noise == NoiseLevel.N0:
            return "09e0af44f0f9862abae3816d7069604a"
        elif noise == NoiseLevel.N10:
            return "64d5300073e02c9651ec88c368c302e8"
        else:
            return "b8fbb96026bd10fd034b8c1270f6edbb"

    @staticmethod
    def _get_size(noise: NoiseLevel) -> float:
        if noise == NoiseLevel.N0:
            return 47.0
        elif noise == NoiseLevel.N10:
            return 282.0
        else:
            return 293.0


class MouseNuclei(PortfolioEntry, NoisyObject):
    """Mouse nuclei dataset used by DenoiSeg.

    The dataset is available in three different noise levels: N0, N10 and N20.


    Attributes
    ----------
    noise_level (NoiseLevel): Noise level of the dataset.
    """

    def __init__(self, noise_level: NoiseLevel = NoiseLevel.N0) -> None:
        """Initialize a MouseNuclei instance.

        Parameters
        ----------
        noise_level : NoiseLevel, optional
            Noise level of the dataset, by default NoiseLevel.N0
        """
        super().__init__(
            noise_level=noise_level,
            name=f"MouseNuclei_n{noise_level.value}",
            url=self._get_url(noise_level),
            file_name=f"MouseNuclei_n{noise_level.value}.zip",
            md5_hash=self._get_hash(noise_level),
            description="A dataset depicting diverse and non-uniformly "
            "clustered nuclei in the mouse skull, consisting of 908 training "
            "and 160 validation patches. The test set counts 67 additional images",
            license="CC BY-SA 4.0",
            citation="Buchholz, T.O., Prakash, M., Schmidt, D., Krull, A., Jug, "
            "F.: Denoiseg: joint denoising and segmentation. In: European "
            "Conference on Computer Vision (ECCV). pp. 324-337. Springer (2020) 8, 9",
            files={
                f"Mouse_n{noise_level.value}/train": ["train_data.npz"],
                f"Mouse_n{noise_level.value}/test": ["test_data.npz"],
            },
            size=self._get_size(noise_level),
        )

    @staticmethod
    def _get_url(noise: NoiseLevel) -> str:
        if noise == NoiseLevel.N0:
            return "https://zenodo.org/record/5157001/files/Mouse_n0.zip?download=1"
        elif noise == NoiseLevel.N10:
            return "https://zenodo.org/record/5157003/files/Mouse_n10.zip?download=1"
        else:
            return "https://zenodo.org/record/5157008/files/Mouse_n20.zip?download=1"

    @staticmethod
    def _get_hash(noise: NoiseLevel) -> str:
        if noise == NoiseLevel.N0:
            return "b747d013cba186a02c97937acef4b972"
        elif noise == NoiseLevel.N10:
            return "0b0776fa205057b49920b0ec3d1a5fc9"
        else:
            return "6e9d895ba3ac2c225883ed3ec94342f8"

    @staticmethod
    def _get_size(noise: NoiseLevel) -> float:
        if noise == NoiseLevel.N0:
            return 12.4
        elif noise == NoiseLevel.N10:
            return 161.0
        else:
            return 160.0
