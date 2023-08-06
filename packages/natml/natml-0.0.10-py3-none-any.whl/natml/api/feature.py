# 
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from dataclasses import dataclass
from typing import List

from .dtype import Dtype

@dataclass
class Feature:
    """
    Prediction feature.

    Members:
        data (str): Feature data URL.
        type (Dtype): Feature data type.
        shape (list): Feature shape. This is `None` if shape information is not available or applicable.
    """
    data: str
    type: Dtype
    shape: List[int] = None