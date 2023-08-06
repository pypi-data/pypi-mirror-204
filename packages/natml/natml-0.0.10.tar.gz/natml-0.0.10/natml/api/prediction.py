# 
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from __future__ import annotations
from base64 import b64encode
from dataclasses import asdict, dataclass
from io import BytesIO
from numpy import frombuffer, ndarray
from PIL import Image
from requests import get
from typing import List, Optional, Union
from urllib.request import urlopen

from .api import query
from .dtype import Dtype
from .feature import Feature

@dataclass
class FeatureInput:
    """
    Prediction input feature.

    Members:
        name (str): Feature name. This MUST match the input parameter name defined by the predictor endpoint.
        data (str): Feature data URL. This can be a web URL or a data URL.
        type (Dtype): Feature data type.
        shape (list): Feature shape. This MUST be provided for array features.
    """
    name: str
    data: str = None
    type: Dtype = None
    shape: Optional[List[int]] = None
    stringValue: str = None
    floatValue: float = None
    floatArray: List[float] = None
    intValue: int = None
    intArray: List[int] = None
    boolValue: bool = None
    listValue: list = None
    dictValue: dict = None

    @classmethod
    def from_value (
        cls,
        value: Union[ndarray, str, float, int, bool, list, dict, Image.Image],
        name: str
    ) -> FeatureInput:
        """
        Create a feature input from a given value.
        
        Parameters:
            value (any): Value.
            name (str): Feature name.

        Returns:
            FeatureInput: Feature input.
        """
        # Array
        if isinstance(value, ndarray):
            encoded_data = b64encode(value).decode("ascii")
            data = f"data:application/octet-stream;base64,{encoded_data}"
            return FeatureInput(name, data, value.dtype.name, list(value.shape))
        # String
        if isinstance(value, str):
            return FeatureInput(name, stringValue=value)
        # Float
        if isinstance(value, float):
            return FeatureInput(name, floatValue=value)
        # Boolean
        if isinstance(value, bool):
            return FeatureInput(name, boolValue=value)
        # Integer
        if isinstance(value, int):
            return FeatureInput(name, intValue=value)
        # List
        if isinstance(value, list):
            return FeatureInput(name, listValue=value)
        # Dict
        if isinstance(value, dict):
            return FeatureInput(name, dictValue=value)
        # Image
        if isinstance(value, Image.Image):
            image_buffer = BytesIO()
            channels = { "L": 1, "RGB": 3, "RGBA": 4 }[value.mode]
            format = "PNG" if value.mode == "RGBA" else "JPEG"
            value.save(image_buffer, format=format)
            encoded_data = b64encode(image_buffer.getvalue()).decode("ascii")
            data = f"data:{value.get_format_mimetype()};base64,{encoded_data}"
            shape = [1, value.height, value.width, channels]
            return FeatureInput(name, data, Dtype.image, shape)
        # Unsupported
        raise RuntimeError(f"Cannot create input feature for value {value} of type {type(value)}")

@dataclass
class PredictionSession:
    """
    Predictor endpoint session.

    Members:
        id (str): Session ID.
        predictor (Predictor): Predictor for which this session was created.
        created (str): Date created.
        results (list): Prediction results.
        latency (float): Prediction latency in milliseconds.
        error (str): Prediction error. This is `null` if the prediction completed successfully.
        logs (str): Prediction logs.
    """
    id: str
    created: str
    results: List[Feature]
    latency: float
    error: str
    logs: str

    @classmethod
    def create (
        cls,
        tag: str,
        *features: List[FeatureInput],
        raw_outputs: bool=False,
        access_key: str=None,
        **inputs,
    ) -> PredictionSession:
        """
        Create an endpoint prediction session.

        Parameters:
            tag (str): Endpoint tag.
            features (list): Input features.
            raw_outputs (bool): Skip parsing output features into Pythonic data types.
            access_key (str): NatML access key.
            inputs (dict): Input features.

        Returns:
            PredictionSession: Prediction session.
        """
        # Collect input features
        input_features = list(features) + [FeatureInput.from_value(value, name) for name, value in inputs.items()]
        input_features = [asdict(feature) for feature in input_features]
        # Query
        parsed_fields = "" if raw_outputs else "\n".join(_FEATURE_KEYS)
        response = query(f"""
            mutation ($input: CreatePredictionSessionInput!) {{
                createPredictionSession (input: $input) {{
                    id
                    created
                    results {{
                        data
                        type
                        shape
                        {parsed_fields}
                    }}
                    latency
                    error
                    logs
                }}
            }}""",
            { "input": { "tag": tag, "inputs": input_features, "client": "python" } },
            access_key=access_key
        )
        # Check session
        session = response["createPredictionSession"]
        if not session:
            return None
        # Parse outputs
        session["results"] = [_parse_output_feature(feature) for feature in session["results"]] if session["results"] and not raw_outputs else session["results"]
        session = PredictionSession(**session)
        # Return
        return session

def _parse_output_feature (feature: dict) -> Union[Feature, str, float, int, bool, Image.Image, list, dict]:
    data, type, shape = feature["data"], feature["type"], feature["shape"]
    # Handle image
    if type == Dtype.image:
        return Image.open(_download_feature_data(data))
    # Handle non-numeric scalars
    values = [feature.get(key, None) for key in _FEATURE_KEYS]
    scalar = next((value for value in values if value is not None), None)
    if scalar is not None:
        return scalar
    # Handle ndarray
    ARRAY_TYPES = [
        Dtype.int8, Dtype.int16, Dtype.int32, Dtype.int64,
        Dtype.uint8, Dtype.uint16, Dtype.uint32, Dtype.uint64,
        Dtype.float16, Dtype.float32, Dtype.float64, Dtype.bool
    ]
    if type in ARRAY_TYPES:
        # Create array
        array = frombuffer(_download_feature_data(data).getbuffer(), dtype=type).reshape(shape)
        return array if len(shape) > 0 else array.item()
    # Handle generic feature
    feature = Feature(**feature)
    return feature

def _download_feature_data (url: str) -> BytesIO:
    # Check if data URL
    if url.startswith("data:"):
        with urlopen(url) as response:
            return BytesIO(response.read())
    # Download
    response = get(url)
    result = BytesIO(response.content)
    return result

_FEATURE_KEYS = ["stringValue", "listValue", "dictValue"]