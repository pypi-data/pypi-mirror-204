# 
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from __future__ import annotations
from dataclasses import dataclass

from .api import query
from .graph import GraphFormat
from .predictor import Predictor

@dataclass
class PredictorSession:
    """
    Predictor graph session.

    Members:
        id (str): Session ID.
        predictor (Predictor): Predictor for which this session was created.
        graph (str): Session graph. This URL is only valid for 10 minutes.
        format (GraphFormat): Session graph format.
        flags (int): Session flags.
        fingerprint (str): Session graph fingerprint. This token uniquely identifies a graph across sessions.
        created (str): Date created.
    """
    id: str
    predictor: Predictor
    graph: str
    format: GraphFormat
    flags: int
    fingerprint: str
    created: str

    def __post_init__ (self):
        self.predictor = Predictor(**self.predictor) if isinstance(self.predictor, dict) else self.predictor

    @classmethod
    def create (
        cls,
        tag: str,
        format: GraphFormat,
        access_key: str=None
    ) -> PredictorSession:
        """
        Create a graph prediction session.

        Parameters:
            tag (str): Graph tag.
            format (GraphFormat): Graph format.
            access_key (str): NatML access key.

        Returns:
            PredictorSession: Predictor session.
        """
        # Query
        response = query(f"""
            mutation ($input: CreatePredictorSessionInput!) {{
                createPredictorSession (input: $input) {{
                    id
                    predictor {{
                        tag
                        owner {{
                            username
                        }}
                        name
                        description
                        status
                        access
                        license
                    }}
                    graph
                    format
                    flags
                    fingerprint
                    created
                }}
            }}
            """,
            { "input": { "tag": tag, "format": format, "client": "python" } },
            access_key=access_key
        )
        # Create session
        session = response["createPredictorSession"]
        session = PredictorSession(**session)
        # Return
        return session