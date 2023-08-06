from http import HTTPStatus
import tempfile
import requests
import numpy as np
from typing import BinaryIO, List, Any
import io


def create_random_vectors(nvects: int, dim: int) -> List[List[float]]:
    return [np.random.rand(dim).tolist() for _ in range(nvects)]

def check_ok(resp: requests.Response):
    if resp.status_code != HTTPStatus.OK:
        raise RuntimeError(resp.json())

def is_file_like(obj: Any) -> bool:
    """Does the object appear to be a file?

    Args:
        obj (Any): The object in question

    Returns:
        [bool]: True if is file like else False
    """
    return isinstance(obj, io.TextIOBase) or \
                isinstance(obj, io.BufferedIOBase) or \
                isinstance(obj, io.RawIOBase) or \
                isinstance(obj, io.IOBase)


def to_tmpfile(_input: bytes) -> BinaryIO:
    """Write a sequence of bytes a temporary file

    Args:
        _input (bytes): The data to be written to temp file

    Returns:
        [BinaryIO]: The temporary file that is closed when garbage collectede
    """
    fp = tempfile.TemporaryFile()
    fp.write(_input)
    fp.seek(0)
    return fp