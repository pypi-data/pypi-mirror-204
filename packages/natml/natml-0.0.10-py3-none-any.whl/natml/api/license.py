# 
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from enum import Enum

class License (str, Enum):
    """
    Predictor license.
    """
    OpenRAIL = "openrail"
    Apache20 = "apache-2.0"
    BSD = "bsd"
    BSD2Clause = "bsd-2-clause"
    BSD3Clause = "bsd-3-clause"
    AGPLv3 = "agpl-3.0"
    GPL = "gpl"
    GPLv2 = "gpl-2.0"
    GPLv3 = "gpl-3.0"
    LGPL = "lgpl"
    LGPLv21 = "lgpl-2.1"
    LGPLv3 = "lgpl-3.0"
    ISC = "isc"
    MIT = "mit"
    OSLv3 = "osl-3.0"
    Unlicense = "unlicense"
    Unknown = "unknown"
    Other = "other" 
    WTFPL = "wtfpl"
    CreativeCommons = "cc"
    CreativeCommons0v10 = "cc0-1.0"
    CreativeCommonsv20 = "cc-by-2.0"
    CreativeCommonsv25 = "cc-by-2.5"
    CreativeCommonsv30 = "cc-by-3.0"
    CreativeCommonsv40 = "cc-by-4.0"
    CreativeCommonsShareAlikev30 = "cc-by-sa-3.0"
    CreativeCommonsShareAlike40 = "cc-by-sa-4.0"
    CreativeCommonsNonCommercialv20 = "cc-by-nc-2.0"
    CreativeCommonsNonCommercialv30 = "cc-by-nc-3.0"
    CreativeCommonsNonCommercialv40 = "cc-by-nc-4.0"
    CreativeCommonsNoDerivativesv40 = "cc-by-nd-4.0"
    CreativeCommonsNonCommercialNoDerivativesv30 = "cc-by-nc-nd-3.0"
    CreativeCommonsNonCommercialNoDerivativesv40 ="cc-by-nc-nd-4.0"
    CreativeCommonsNonCommercialShareAlikev20 = "cc-by-nc-sa-2.0"
    CreativeCommonsNonCommercialShareAlikev30 = "cc-by-nc-sa-3.0"
    CreativeCommonsNonCommercialShareAlikev40 = "cc-by-nc-sa-4.0"