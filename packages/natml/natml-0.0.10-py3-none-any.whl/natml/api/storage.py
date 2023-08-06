# 
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from enum import Enum
from io import BytesIO
from mimetypes import guess_type
from pathlib import Path
from requests import put
from rich.progress import open as open_progress
from typing import Union

from .api import query

class UploadType (str, Enum):
    """
    Upload URL type.
    """
    Demo = "DEMO"
    Feature = "FEATURE"
    Graph = "GRAPH"
    Media = "MEDIA"
    Notebook = "NOTEBOOK"

class Storage:
    """
    Upload and download files.
    """

    @classmethod
    def create_upload_url (
        cls,
        name: str,
        type: UploadType,
        key: str=None
    ) -> str:
        """
        Create an upload URL.

        Parameters:
            name (str): File name.
            type (UploadType): Upload type.
            key (str): File key. This is useful for grouping related files.

        Returns:
            str: File upload URL.
        """
        # Query
        response = query(f"""
            mutation ($input: CreateUploadURLInput!) {{
                createUploadURL (input: $input)
            }}
            """,
            { "input": { "type": type, "name": name, "key": key } }
        )
        url = response["createUploadURL"]
        # Return
        return url

    @classmethod
    def upload ( # INCOMPLETE # `bytes` and `BytesIO` support` # Min upload size
        cls,
        file: Union[str, Path, BytesIO, bytes],
        type: UploadType,
        name: str=None,
        key: str=None,
        min_upload_size: int=0,
        check_extension: bool=True,
        verbose: bool=False
    ) -> str:
        """
        Upload a file and return the URL.

        Parameters:
            file (str | Path | BytesIO | bytes): File path.
            type (UploadType): File type.
            name (str): File name. This MUST be provided if `file` is not a file path.
            key (str): File key. This is useful for grouping related files.
            min_upload_size (int): Minimum file size for file to be uploaded. Files smaller than this limit will be returned as data URLs.
            check_extension (bool): Validate file extensions before uploading.

        Returns:
            str: Upload URL.
        """
        EXTENSIONS = {
            UploadType.Demo: [".data", ".js", ".wasm"],
            UploadType.Feature: [],
            UploadType.Graph: [".mlmodel", ".onnx", ".tflite", ".pt", ".pth"],
            UploadType.Media: [".jpg", ".jpeg", ".png", ".gif"],
            UploadType.Notebook: [".ipynb"],
        }
        # Create path
        file = Path(file) if isinstance(file, str) else file
        # Check path
        if not file.exists():
            raise RuntimeError(f"Cannot upload {file.name} because the file does not exist")
        # Check file
        if not file.is_file():
            raise RuntimeError(f"Cannot upload {file.name} becaause it does not point to a file")
        # Check extension
        if check_extension and file.suffix not in EXTENSIONS[type]:
            raise RuntimeError(f"Cannot upload {file.name} because it is not a valid {type.name.lower()} file")
        # Get upload URL
        mime = guess_type(file, strict=False)[0] or "application/octet-stream"
        url = cls.create_upload_url(file.name, type, key=key)
        with open_progress(file, "rb", description=file.name, disable=not verbose) as f:
            put(url, data=f, headers={ "Content-Type": mime }).raise_for_status()
        # Return
        return url