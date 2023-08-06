import os
import re
import urllib
from pathlib import Path
from typing import Iterator

USER_AGENT = "minopt"


def _get_model_dir() -> Path:
    model_dir_env = os.environ.get("MODEL_DIR_NAME", "MODEL_DIR")
    if model_dir_env in os.environ:
        return Path(os.environ["MODEL_DIR"])
    raise KeyError(
        "In order to download a pre-trained model, first set the `MODEL_DIR` "
        "environment variable to point to the directory where you would like to "
        "download the model weights. Alternatively, you can set `MODEL_DIR_NAME` "
        "to the name of some environment variable that points to your model "
        "directory, such as `HF_HOME`"
    )


def _save_response_content(content: Iterator[bytes], destination: str) -> None:
    with open(destination, "wb") as fh:
        for chunk in content:
            if not chunk:
                continue
            fh.write(chunk)


def _urlretrieve(url: str, filename: str, chunk_size: int = 1024 * 32) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request) as response:
        _save_response_content(iter(lambda: response.read(chunk_size), b""), filename)


def _get_redirect_url(url: str, max_hops: int = 3) -> str:
    initial_url = url
    headers = {"Method": "HEAD", "User-Agent": USER_AGENT}

    for _ in range(max_hops + 1):
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as response:
            if response.url == url or response.url is None:
                return url
            url = response.url
    raise RecursionError(
        f"Request to {initial_url} exceeded {max_hops} redirects. " f"The last redirect points to {url}."
    )


def download_url(url: str, root: str, filename: str | None = None, max_redirect_hops: int = 3) -> None:
    """Download a file from a url and place it in root.

    This function and it's subfunctions are mostly copied from the TorchVision
    implementation: `torchvision.datasets.utils.download_url`

    Args:
        url: URL to download file from
        root: Directory to place downloaded file in
        filename: Name to save the file under. If None, use the basename of the URL
        max_redirect_hops: Maximum number of redirect hops allowed

    Raises:
        OSError: If there is an error dowloading the requested URL
    """

    root = os.path.expanduser(root)
    if not filename:
        filename = os.path.basename(url)
    fpath = os.path.join(root, filename)

    os.makedirs(root, exist_ok=True)

    # expand redirect chain if needed
    url = _get_redirect_url(url, max_hops=max_redirect_hops)

    # download the file
    try:
        print("Downloading " + url + " to " + fpath)
        _urlretrieve(url, fpath)
    except (urllib.error.URLError, OSError) as e:
        if url[:5] == "https":
            url = url.replace("https:", "http:")
            print("Failed download. Trying https -> http instead. Downloading " + url + " to " + fpath)
            _urlretrieve(url, fpath)
        else:
            raise e


def download_sharded_weights(urls: list[str]) -> list[Path]:
    """Downloads the sharded OPT weights and returns their location.

    Args:
        urls: The URLs of the sharded weights files to download

    Returns:
        The path of the downloaded weights
    """

    # Parses a unique identifier from the URLs.
    match = re.search(r".com/(.+)$", urls[0])
    assert match is not None
    identifier = os.path.dirname(match.group(1))
    assert all(identifier in url for url in urls)
    identifier = "_".join(i.upper() for i in identifier.split("/"))

    # All files are downloaded to the same directory.
    root = (_get_model_dir() / identifier).resolve()
    filepaths: list[Path] = []

    for url in urls:
        filename = os.path.basename(url)
        filepath = root / filename
        filepaths.append(filepath)
        if not filepath.exists():
            download_url(url, str(root), filename=filename)

    return filepaths
