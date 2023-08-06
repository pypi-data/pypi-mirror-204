# 
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from os import environ

# Define API URL and access key
api_url = "https://staging.api.natml.ai/graph" if environ.get("NATML_STAGING", None) else "https://api.natml.ai/graph"
access_key: str = environ.get("NATML_ACCESS_KEY", None)

# Import everything
from .api import *
from .version import __version__