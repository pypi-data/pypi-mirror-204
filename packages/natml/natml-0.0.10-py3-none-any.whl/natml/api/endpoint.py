# 
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional, Tuple, Union

from .api import query
from .dtype import Dtype
from .storage import Storage, UploadType
from .tag import Tag, parse_tag, serialize_tag

class EndpointType (str, Enum):
    """
    Endpoint type.
    """
    Serverless = "SERVERLESS"
    Dedicated = "DEDICATED"

class EndpointAcceleration (str, Enum):
    """
    Endpoint acceleration.
    """
    CPU = "CPU"
    A40 = "A40"
    A100 = "A100"

class EndpointStatus (str, Enum):
    """
    Endpoint status.
    """
    Provisioning = "PROVISIONING"
    Active = "ACTIVE"
    Invalid = "INVALID"

@dataclass
class EndpointParameter:
    """
    Endpoint parameter.

    Members:
        name (str): Parameter name. This is only populated for input parameters.
        type (Dtype): Parameter type. This is `None` if the type is unknown or unsupported by NatML.
        description (str): Parameter description.
        optional (bool): Parameter is optional.
        range (tuple): Parameter value range for numeric parameters.
        stringDefault (str): Parameter default string value.
        floatDefault (float): Parameter default float value.
        intDefault (int): Parameter default integer value.
        boolDefault (bool): Parameter default boolean value.
    """
    name: Optional[str] = None
    type: Optional[Dtype] = None
    description: Optional[str] = None
    optional: Optional[bool] = None
    range: Optional[Tuple[float, float]] = None
    string_default: Optional[str] = None
    float_default: Optional[float] = None
    int_default: Optional[int] = None
    bool_default: Optional[bool] = None

@dataclass
class EndpointSignature:
    """
    Endpoint signature.

    Members:
        inputs (list): Input parameters.
        outputs (list): Output parameters.
    """
    inputs: List[EndpointParameter]
    outputs: List[EndpointParameter]

    def __post_init__ (self):
        self.inputs = [EndpointParameter(**parameter) if isinstance(parameter, dict) else parameter for parameter in self.inputs]
        self.outputs = [EndpointParameter(**parameter) if isinstance(parameter, dict) else parameter for parameter in self.outputs]

@dataclass
class Endpoint:
    """
    Predictor endpoint.

    Members:
        variant (str): Endpoint variant.
        url (str): Endpoint URL.
        type (EndpointType): Endpoint type.
        acceleration (EndpointAcceleration): Endpoint acceleration.
        status (EndpointStatus): Endpoint status.
        created (str): Date created.
        signature (EndpointSignature): Endpoint prediction signature. This is populated for `ACTIVE` endpoints.
        error (str): Endpoint error. This is populated for `INVALID` endpoints.
    """
    variant: str
    url: str
    type: EndpointType
    acceleration: EndpointAcceleration
    status: EndpointStatus
    created: str
    signature: EndpointSignature
    error: str
    FIELDS = f"""
    variant
    url
    type
    acceleration
    status
    created
    signature {{
        inputs {{
            name
            type
            description
            range
            optional
            string_default: stringDefault
            float_default: floatDefault
            int_default: intDefault
            bool_default: boolDefault
        }}
        outputs {{
            name
            type
            description
            range
            optional
            string_default: stringDefault
            float_default: floatDefault
            int_default: intDefault
            bool_default: boolDefault
        }}
    }}
    error
    """

    def __post_init__ (self):
        self.signature = EndpointSignature(**self.signature) if isinstance(self.signature, dict) else self.signature

    @classmethod
    def retrieve (
        cls,
        tag: str,
        access_key: str=None
    ) -> Endpoint:
        """
        Retrieve a predictor endpoint.

        Parameters:
            tag (str): Endpoint tag. If the tag does not contain a variant then the variant defaults to `main`.
            access_key (str): NatML access key.

        Returns:
            Endpoint: Predictor endpoint.
        """
        # Ensure this is a predictor tag
        tag = parse_tag(tag)
        variant = tag.variant or "main"
        tag = Tag(tag.username, tag.name)
        tag = serialize_tag(tag)
        # There isn't a query to get a specific endpoint so just filter for now
        endpoints = cls.list(tag, access_key=access_key)
        endpoint = next((x for x in endpoints if x.variant == variant), None) if endpoints else None
        # Return
        return endpoint

    @classmethod
    def list (
        cls,
        tag: str,
        access_key: str=None
    ) -> List[Endpoint]:
        """
        Retrieve all predictor endpoints.

        Parameters:
            tag (str): Predictor tag. This MUST NOT be a variant tag.
            access_key (str): NatML access key.

        Returns:
            list: Predictor endpoints.
        """
        # Request
        response = query(f"""
            query ($input: PredictorInput!) {{
                predictor (input: $input) {{
                    endpoints {{
                        {Endpoint.FIELDS}
                    }}
                }}
            }}""",
            { "input": { "tag": tag } },
            access_key=access_key
        )
        # Check predictor
        predictor = response["predictor"]
        if not predictor:
            return None
        # Get endpoints
        endpoints = [Endpoint(**endpoint) for endpoint in predictor["endpoints"]]
        return endpoints

    @classmethod
    def create (
        cls,
        tag: str,
        notebook: Union[str, Path],
        type: EndpointType,
        acceleration: EndpointAcceleration,
        access_key: str=None
    ) -> Endpoint:
        """
        Create a predictor endpoint.

        Parameters:
            tag (str): Endpoint tag. If the tag does not contain a variant then the variant defaults to `main`.
            notebook (str | Path): Notebook URL or path.
            type (EndpointType): Endpoint type.
            acceleration (EndpointAcceleration): Endpoint acceleration.
            access_key (str): NatML access key.

        Returns:
            Endpoint: Created endpoint.
        """
        # Upload notebook
        url = Storage.upload(notebook, UploadType.Notebook, check_extension=True) if isinstance(notebook, Path) else notebook
        # Query
        response = query(f"""
            mutation ($input: CreateEndpointInput!) {{
                createEndpoint (input: $input) {{
                    {Endpoint.FIELDS}
                }}
            }}""",
            { "input": { "tag": tag, "notebook": url, "type": type, "acceleration": acceleration } },
            access_key=access_key
        )
        # Create endpoint
        endpoint = response["createEndpoint"]
        endpoint = Endpoint(**endpoint)
        # Return
        return endpoint

    @classmethod
    def delete (
        cls,
        tag: str,
        access_key: str=None
    ) -> bool:
        """
        Delete a predictor endpoint.

        Parameters:
            tag (str): Endpoint tag. If the tag does not contain a variant then the variant defaults to `main`.
            access_key (str): NatML access key.

        Returns:
            bool: Whether the endpoint was successfully deleted.
        """
        # Query
        response = query(f"""
            mutation ($input: DeleteEndpointInput!) {{
                deleteEndpoint (input: $input)
            }}""",
            { "input": { "tag": tag } },
            access_key=access_key
        )
        # Return
        result = response["deleteEndpoint"]
        return result