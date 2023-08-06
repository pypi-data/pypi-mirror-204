# 
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from dataclasses import asdict
from filetype import image_match
from io import BytesIO
from numpy import ndarray
from pathlib import Path
from PIL import Image
from rich import print_json
from tempfile import mkstemp
from typer import Argument, Context, Option, Typer
from typing import Union

from ..api import Endpoint, EndpointType, EndpointAcceleration, PredictionSession
from .auth import get_access_key
from .misc import create_learn_callback

app = Typer(no_args_is_help=True)

@app.command(name="retrieve", help="Retrieve a predictor endpoint.")
def retrieve_endpoint (
    tag: str=Argument(..., help="Endpoint tag. If the tag does not contain a variant then the variant defaults to `main`.")
) -> None:
    endpoint = Endpoint.retrieve(tag, access_key=get_access_key())
    endpoint = asdict(endpoint) if endpoint else None
    print_json(data=endpoint)

@app.command(name="list", help="List all predictor endpoints.")
def list_endpoints (
    tag: str=Argument(..., help="Predictor tag. This MUST NOT be a variant tag.")
) -> None:
    endpoints = Endpoint.list(tag, access_key=get_access_key())
    endpoints = [asdict(endpoint) for endpoint in endpoints] if endpoints else None
    print_json(data=endpoints)

@app.command(name="create", help="Create a predictor endpoint.")
def create_endpoint (
    tag: str=Argument(..., help="Endpoint tag."),
    notebook: Path=Argument(..., help="Path to endpoint notebook."),
    type: EndpointType=Option(EndpointType.Serverless, case_sensitive=False, help="Endpoint type."),
    acceleration: EndpointAcceleration=Option(EndpointAcceleration.CPU, case_sensitive=False, help="Endpoint acceleration."),
) -> None:
    endpoint = Endpoint.create(tag, notebook, type, acceleration, access_key=get_access_key())
    endpoint = asdict(endpoint)
    print_json(data=endpoint)

@app.command(name="delete", help="Delete a predictor endpoint.")
def delete_endpoint (
    tag: str=Argument(..., help="Endpoint tag.")
) -> None:
    result = Endpoint.delete(tag, access_key=get_access_key())
    print_json(data=result)

@app.command(
    name="predict",
    context_settings={ "allow_extra_args": True, "ignore_unknown_options": True },
    help="Make a prediction with a predictor endpoint."
)
def predict (
    tag: str = Argument(..., help="Endpoint tag."),
    raw_outputs: bool = Option(False, "--raw-outputs", help="Generate raw output features instead of parsing."),
    context: Context = 0
) -> None:
    inputs = { context.args[i].replace("-", ""): _parse_value(context.args[i+1]) for i in range(0, len(context.args), 2) }
    session = PredictionSession.create(tag, **inputs, raw_outputs=raw_outputs, access_key=get_access_key())
    images = [feature for feature in session.results if isinstance(feature, Image.Image)] if session.results is not None else []
    session.results = [_serialize_feature(feature) for feature in session.results] if session.results is not None else None
    print_json(data=asdict(session))
    for image in images:
        image.show()

@app.callback()
def endpoint_options (
    learn: bool = Option(None, "--learn", callback=create_learn_callback("https://docs.natml.ai/graph/endpoints/type"), help="Learn about predictor endpoints in NatML.")
):
    pass

def _parse_value (value: str):
    """
    Parse a value from a CLI argument.

    Parameters:
        value (str): CLI input argument.

    Returns:
        bool | int | float | str | Path: Parsed value.
    """
    # Boolean
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    # Integer
    try:
        return int(value)
    except ValueError:
        pass
    # Float
    try:
        return float(value)
    except ValueError:
        pass
    # File
    if value.startswith("@"):
        return _parse_file(Path(value[1:]))
    # String
    return value

def _parse_file (path: Path) -> Union[Image.Image, BytesIO]:
    """
    Parse a file from a given path.

    Parameters:
        path (Path): File path.

    Returns:
        Image | BytesIO: File.
    """
    # Load image
    if image_match(path):
        return Image.open(path)
    # Load buffer
    with open(path, "rb") as f:
        return BytesIO(f.read())
    
def _serialize_feature (feature):
    # Convert ndarray to list
    if isinstance(feature, ndarray):
        return feature.tolist()
    # Write image
    if isinstance(feature, Image.Image):
        _, path = mkstemp(suffix=".png" if feature.mode == "RGBA" else ".jpg")
        feature.save(path)
        return path
    # Return    
    return feature