# 
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from typing import NamedTuple, Optional

class Tag (NamedTuple):
    """
    Predictor tag.

    Members:
        username (str): Username.
        name (str): Name.
        variant (str): Variant.
    """
    username: str
    name: str
    variant: Optional[str] = None

def parse_tag (tag: str) -> Tag:
    """
    Parse a predictor tag.

    Parameters:
        tag (str): Tag string.

    Returns:
        Tag: Parsed tag.
    """
    username, full_name = tag.lower()[1:].split("/")
    name_components = full_name.split("@")
    name = name_components[0]
    variant = name_components[1] if len(name_components) > 1 else None
    result = Tag(username=username, name=name, variant=variant)
    return result

def serialize_tag (tag: Tag) -> str:
    """
    Serialize a predictor tag.

    Parameters:
        tag (Tag): Tag.

    Returns:
        str: Serialized tag.
    """
    username, name, variant = tag
    suffix = f"@{variant}" if variant else ""
    result = f"@{username}/{name}{suffix}"
    return result