# 
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Union

from .api import query
from .storage import Storage, UploadType
from .tag import Tag, parse_tag, serialize_tag

class GraphFormat (str, Enum):
    """
    Graph format.
    """
    CoreML = "COREML"
    ONNX = "ONNX"
    TFLite = "TFLITE"

class GraphStatus (str, Enum):
    """
    Graph status.
    """
    Provisioning = "PROVISIONING"
    Active = "ACTIVE"
    Invalid = "INVALID"

@dataclass
class Graph:
    """
    Predictor graph.

    Members:
        variant (str): Graph variant.
        format (GraphFormat): Graph format.
        status (GraphStatus): Graph status.
        encrypted (bool): Whether the graph is encrypted.
        created (str): Date created.
        error (str): Graph provisioning error. This is populated when the graph `status` is `INVALID`.
    """
    variant: str
    format: GraphFormat
    status: GraphStatus
    encrypted: bool
    created: str
    error: str
    FIELDS = f"""
    variant
    format
    status
    encrypted
    created
    error
    """

    @classmethod
    def retrieve (
        cls,
        tag: str,
        format: GraphFormat,
        access_key: str=None
    ) -> Graph:
        """
        Retrieve a predictor graph.

        Parameters:
            tag (str): Graph tag. If the tag does not contain a variant then the variant defaults to `main`.
            format (GraphFormat): Graph format.
            access_key (str): NatML access key.

        Returns:
            Graph: Predictor graph.
        """
        # Ensure this is a predictor tag
        tag = parse_tag(tag)
        variant = tag.variant or "main"
        tag = Tag(tag.username, tag.name)
        tag = serialize_tag(tag)
        # There isn't a query to get a specific graph so just filter for now
        graphs = cls.list(tag, access_key=access_key)
        graph = next((x for x in graphs if x.variant == variant and x.format == format), None) if graphs else None
        # Return
        return graph

    @classmethod
    def list (
        cls,
        tag: str,
        access_key: str=None
    ) -> List[Graph]:
        """
        Retrieve all predictor graphs.

        Parameters:
            tag (str): Predictor tag. This MUST NOT be a variant tag.
            access_key (str): NatML access key.

        Returns:
            list: Predictor graphs.
        """
        # Request
        response = query(f"""
            query ($input: PredictorInput!) {{
                predictor (input: $input) {{
                    graphs {{
                        {Graph.FIELDS}
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
        # Get graphs
        graphs = [Graph(**graph) for graph in predictor["graphs"]]
        return graphs

    @classmethod
    def create (
        cls,
        tag: str,
        graph: Union[str, Path],
        format: GraphFormat,
        access_key: str=None
    ) -> Graph:
        """
        Create a predictor graph.

        Parameters:
            tag (str): Graph tag. If the tag does not contain a variant then the variant defaults to `main`.
            graph (str | Path): Source graph URL or path.
            format (GraphFormat): Target graph format.
            access_key (str): NatML access key.

        Returns:
            Graph: Created graph.
        """
        # Upload graph
        url = Storage.upload(graph, UploadType.Graph, check_extension=True) if isinstance(graph, Path) else graph
        # Query
        response = query(f"""
            mutation ($input: CreateGraphInput!) {{
                createGraph (input: $input) {{
                    {Graph.FIELDS}
                }}
            }}""",
            { "input": { "tag": tag, "graph": url, "format": format } },
            access_key=access_key
        )
        # Create endpoint
        graph = response["createGraph"]
        graph = Graph(**graph)
        # Return
        return graph

    @classmethod
    def delete (
        cls,
        tag: str,
        format: GraphFormat,
        access_key: str=None
    ) -> bool:
        """
        Delete a predictor graph.

        Parameters:
            tag (str): Graph tag. If the tag does not contain a variant then the variant defaults to `main`.
            format (GraphFormat): Graph format.
            access_key (str): NatML access key.

        Returns:
            bool: Whether the graph was successfully deleted.
        """
        # Query
        response = query(f"""
            mutation ($input: DeleteGraphInput!) {{
                deleteGraph (input: $input)
            }}""",
            { "input": { "tag": tag, "format": format } },
            access_key=access_key
        )
        # Return
        result = response["deleteGraph"]
        return result