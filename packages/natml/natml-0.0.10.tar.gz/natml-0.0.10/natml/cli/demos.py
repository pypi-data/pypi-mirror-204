# 
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from pathlib import Path
from re import search
from rich import print, print_json
from typer import Argument, Option, Typer
from uuid import uuid4
from webbrowser import open as open_browser

from ..api import Storage, UploadType
from ..api.api import query
from .auth import get_access_key
from .misc import create_learn_callback

app = Typer(no_args_is_help=True)

@app.command(name="create", help="Create a Unity WebGL demo.")
def create_demo (
    tag: str=Argument(..., help="Demo tag."),
    path: Path=Option(None, help="Unity WebGL build directory. This defaults to the current working directory.")
) -> None:
    path = path if path is not None else Path.cwd()
    # Check index
    index = path / "index.html"
    if not index.is_file():
        raise RuntimeError("Count not find WebGL index.html")
    # Get build info
    with open(index) as f:
        source = f.read()
    product = _get_value(source, r"\s*productName:\s*[\"'](\w+)[\"']")
    company = _get_value(source, r"\s*companyName:\s*[\"'](\w+)[\"']")
    version = _get_value(source, r"\s*productVersion:\s*[\"']([\w\d\.]+)[\"']")
    # Get loader
    loader = next((file for file in path.glob("*/*.loader.js") if file.is_file()), None)
    if not loader:
        raise RuntimeError("Could not find WebGL loader script")
    # Get framework
    framework = next((file for file in path.glob("*/*.js") if file.is_file() and "." not in file.stem), None)
    if not framework:
        raise RuntimeError("Count not find WebGL framework script")
    # Get code
    code = next((file for file in path.glob("*/*.wasm") if file.is_file()), None)
    if not code:
        raise RuntimeError("Could not find WebGL WebAssembly binary")
    # Get data
    data = next((file for file in path.glob("*/*.data") if file.is_file()), None)
    if not data:
        raise RuntimeError("Could not find WebGL data file")
    # Upload
    key = uuid4().hex
    verbose = True
    loader = Storage.upload(loader, type=UploadType.Demo, name=loader.name, key=key, verbose=verbose)
    framework = Storage.upload(framework, type=UploadType.Demo, name=framework.name, key=key, verbose=verbose)
    data = Storage.upload(data, type=UploadType.Demo, name=data.name, key=key, verbose=verbose)
    code = Storage.upload(code, type=UploadType.Demo, name=code.name, key=key, verbose=verbose)
    # Create demo
    response = query(f"""
        mutation ($input: CreateDemoInput!) {{
            createDemo (input: $input) {{
                tag
                url
            }}
        }}
        """,
        {
            "input": {
                "tag": tag,
                "product": product,
                "company": company,
                "version": version,
                "loader": loader,
                "framework": framework,
                "code": code,
                "data": data
            }
        },
        access_key=get_access_key()
    )
    # Print
    demo = response["createDemo"]
    print_json(data=demo)

@app.command(name="open", help="Open a demo.")
def open_demo (
    tag: str=Argument(..., help="Demo tag.")
) -> None:
    response = query(f"""
        query ($input: DemoInput!) {{
            demo (input: $input) {{
                tag
                url
            }}
        }}
        """,
        { "input": { "tag": tag } }
    )
    demo = response["demo"]
    if demo:
        open_browser(demo["url"])
    else:
        print("[red italic]Demo was not found[/red italic]")

@app.command(name="delete", help="Delete a demo.")
def delete_demo (
    tag: str=Argument(..., help="Demo tag.")
) -> None:
    response = query(f"""
        mutation ($input: DeleteDemoInput!) {{
            deleteDemo (input: $input)
        }}
        """,
        { "input": { "tag": tag } },
        access_key=get_access_key()
    )
    result = response["deleteDemo"]
    print_json(data=result)

@app.callback()
def demo_options (
    learn: bool = Option(None, "--learn", callback=create_learn_callback("https://docs.natml.ai/graph/demos/type"), help="Learn about predictor demos in NatML.")
):
    pass

def _get_value (source: str, pattern: str) -> str:
    for line in source.splitlines():
        match = search(pattern, line)
        if match:
            return match[1]
    return None