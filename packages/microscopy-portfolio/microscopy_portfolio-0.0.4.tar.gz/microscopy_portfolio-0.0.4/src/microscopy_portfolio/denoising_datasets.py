from .portfolio_entry import PortfolioEntry

# TODO add descriptions in the class docstrings


class N2V_BSD68(PortfolioEntry):
    """BSD68 dataset.

    Attributes
    ----------
    name (str): Name of the dataset.
    url (str): URL of the dataset.
    file_name (str): Name of the downloaded file.
    md5_hash (str): MD5 hash of the downloaded file.
    description (str): Description of the dataset.
    license (str): License of the dataset.
    citation (str): Citation to use when referring to the dataset.
    files (dict): Dictionary containing the files to download.
    size (float): Size of the dataset in MB.
    """

    def __init__(self) -> None:
        super().__init__(
            name="N2V_BSD68",
            url="https://download.fht.org/jug/n2v/BSD68_reproducibility.zip",
            file_name="BSD68_reproducibility.zip",
            md5_hash="292c29895fa56ef7226487005b5955a2",
            description="This dataset is taken from K. Zhang et al (TIP, 2017). \n"
            "It consists of 400 gray-scale 180x180 images (cropped from the "
            "BSD dataset) and splitted between training and validation, and "
            "68 gray-scale test images (BSD68).\n"
            "All images were corrupted with Gaussian noise with standard "
            "deviation of 25 pixels. The test dataset contains the uncorrupted "
            "images as well.\n"
            "Original dataset: "
            "https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/",
            license="Unknown",
            citation='D. Martin, C. Fowlkes, D. Tal and J. Malik, "A database of '
            "human segmented natural images and its application to "
            "evaluating segmentation algorithms and measuring ecological "
            'statistics," Proceedings Eighth IEEE International '
            "Conference on Computer Vision. ICCV 2001, Vancouver, BC, "
            "Canada, 2001, pp. 416-423 vol.2, doi: "
            "10.1109/ICCV.2001.937655.",
            files={
                "BSD68_reproducibility_data/test": [
                    "bsd68_gaussian25.npy",
                    "bsd68_groundtruth.npy",
                ],
                "BSD68_reproducibility_data/train": ["DCNN400_train_gaussian25.npy"],
                "BSD68_reproducibility_data/val": ["DCNN400_validation_gaussian25.npy"],
            },
            size=875.0,
        )


class N2V_SEM(PortfolioEntry):
    """SEM dataset.

    Attributes
    ----------
    name (str): Name of the dataset.
    url (str): URL of the dataset.
    file_name (str): Name of the downloaded file.
    md5_hash (str): MD5 hash of the downloaded file.
    description (str): Description of the dataset.
    license (str): License of the dataset.
    citation (str): Citation to use when referring to the dataset.
    files (dict): Dictionary containing the files to download.
    size (float): Size of the dataset in MB.
    """

    def __init__(self) -> None:
        super().__init__(
            name="N2V_SEM",
            url="https://download.fht.org/jug/n2v/SEM.zip",
            file_name="SEM.zip",
            md5_hash="953a815333805a423b7019bd16cc3341",
            description="Cropped images from a SEM dataset from T.-O. Buchholz et al "
            "(Methods Cell Biol, 2020).",
            license="CC-BY-4.0",
            citation="T.-O. Buchholz, A. Krull, R. Shahidi, G. Pigino, G. Jékely, "
            'F. Jug, "Content-aware image restoration for electron '
            'microscopy", Methods Cell Biol 152, 277-289',
            files={
                ".": ["train.tif", "validation.tif"],
            },
            size=13.0,
        )


class N2V_RGB(PortfolioEntry):
    """RGB dataset.

    Attributes
    ----------
    name (str): Name of the dataset.
    url (str): URL of the dataset.
    file_name (str): Name of the downloaded file.
    md5_hash (str): MD5 hash of the downloaded file.
    description (str): Description of the dataset.
    license (str): License of the dataset.
    citation (str): Citation to use when referring to the dataset.
    files (dict): Dictionary containing the files to download.
    size (float): Size of the dataset in MB.
    """

    def __init__(self) -> None:
        super().__init__(
            name="N2V_RGB",
            url="https://download.fht.org/jug/n2v/RGB.zip",
            file_name="RGB.zip",
            md5_hash="ad80d2fee3ae0a93208687e30ad2b63a",
            description="Banner of the CVPR 2019 conference with extra noise.",
            license="CC-BY-4.0",
            citation='A. Krull, T.-O. Buchholz and F. Jug, "Noise2Void - Learning '
            'Denoising From Single Noisy Images," 2019 IEEE/CVF '
            "Conference on Computer Vision and Pattern Recognition (CVPR),"
            " 2019, pp. 2124-2132",
            files={
                ".": ["longBeach.png"],
            },
            size=10.4,
        )


class Flywing(PortfolioEntry):
    """Flywing dataset.

    Attributes
    ----------
    name (str): Name of the dataset.
    url (str): URL of the dataset.
    file_name (str): Name of the downloaded file.
    md5_hash (str): MD5 hash of the downloaded file.
    description (str): Description of the dataset.
    license (str): License of the dataset.
    citation (str): Citation to use when referring to the dataset.
    files (dict): Dictionary containing the files to download.
    size (float): Size of the dataset in MB.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Flywing",
            url="https://download.fht.org/jug/n2v/flywing-data.zip",
            file_name="flywing-data.zip",
            md5_hash="769f4e265f8ab8ccea1893087df019da",
            description="Image of a membrane-labeled fly wing (35x692x520 pixels).",
            license="CC-BY-4.0",
            citation="Buchholz, T.O., Prakash, M., Schmidt, D., Krull, A., Jug, "
            "F.: Denoiseg: joint denoising and segmentation. In: European "
            "Conference on Computer Vision (ECCV). pp. 324-337. Springer (2020) 8, 9",
            files={
                ".": ["flywing.tif"],
            },
            size=10.2,
        )


class Convallaria(PortfolioEntry):
    """Convallaria dataset.

    Attributes
    ----------
    name (str): Name of the dataset.
    url (str): URL of the dataset.
    file_name (str): Name of the file to download.
    md5_hash (str): MD5 hash of the file to download.
    description (str): Description of the dataset.
    license (str): License of the dataset.
    citation (str): Citation to use when referring to the dataset.
    files (dict): Dictionary containing the files to download.
    size (float): Size of the dataset in MB.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Convallaria",
            url="https://cloud.mpi-cbg.de/index.php/s/BE8raMtHQlgLDF3/download",
            file_name="Convallaria_diaphragm.zip",
            md5_hash="7b8df3a83939decaede6753b8d38b52f",
            description="Image of a convallaria flower (35x692x520 pixels).\n"
            "The image also comes with a defocused image in order to allow \n"
            "estimating the noise distribution.",
            license="CC-BY-4.0",
            citation="Krull, A., Vičar, T., Prakash, M., Lalit, M., & Jug, F. (2020). "
            "Probabilistic noise2void: Unsupervised content-aware denoising. Frontiers"
            " in Computer Science, 2, 5.",
            files={
                "Convallaria_diaphragm": [
                    "20190520_tl_25um_50msec_05pc_488_130EM_Conv.tif",
                    "20190726_tl_50um_500msec_wf_130EM_FD.tif",
                ],
            },
            size=344.0,
        )
