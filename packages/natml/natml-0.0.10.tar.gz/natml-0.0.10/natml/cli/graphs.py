# 
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from dataclasses import asdict
from pathlib import Path
from rich import print_json
from typer import Argument, Context, Option, Typer

from ..api import Graph, GraphFormat, PredictorSession
from .auth import get_access_key
from .misc import create_learn_callback

app = Typer(no_args_is_help=True)

@app.command(name="retrieve", help="Retrieve a predictor graph.")
def retrieve_graph (
    tag: str=Argument(..., help="Graph tag. If the tag does not contain a variant then the variant defaults to `main`."),
    format: GraphFormat=Argument(..., case_sensitive=False, help="Graph format.")
) -> None:
    graph = Graph.retrieve(tag, format, access_key=get_access_key())
    graph = asdict(graph) if graph else None
    print_json(data=graph)

@app.command(name="list", help="List all predictor graphs.")
def list_graph (
    tag: str=Argument(..., help="Predictor tag. This MUST NOT be a variant tag.")
) -> None:
    graphs = Graph.list(tag, access_key=get_access_key())
    graphs = [asdict(graph) for graph in graphs] if graphs else None
    print_json(data=graphs)

@app.command(name="create", help="Create a predictor graph.")
def create_graph (
    tag: str=Argument(..., help="Graph tag. If the tag does not contain a variant then the variant defaults to `main`."),
    graph: Path=Argument(..., help="Path to ML graph."),
    format: GraphFormat=Argument(..., case_sensitive=False, help="Target graph format.")
) -> None:
    graph = Graph.create(tag, graph, format, access_key=get_access_key())
    graph = asdict(graph)
    print_json(data=graph)

@app.command(name="delete", help="Delete a predictor graph.")
def delete_graph (
    tag: str=Argument(..., help="Graph tag. If the tag does not contain a variant then the variant defaults to `main`."),
    format: GraphFormat=Argument(..., case_sensitive=False, help="Graph format.")
) -> None:
    result = Graph.delete(tag, format, access_key=get_access_key())
    print_json(data=result)

@app.command(
    name="predict",
    context_settings={ "allow_extra_args": True, "ignore_unknown_options": True },
    help="Make a prediction with a predictor graph."
)
def predict (
    tag: str = Argument(..., help="Graph tag."),
    raw_outputs: bool = Option(False, "--raw-outputs", help="Generate raw output features instead of parsing."),
    context: Context = 0
) -> None:
    raise RuntimeError("Making edge predictions is not yet supported in NatML Python SDK")

@app.callback()
def graph_options (
    learn: bool = Option(None, "--learn", callback=create_learn_callback("https://docs.natml.ai/graph/graphs/type"), help="Learn about predictor graphs in NatML.")
):
    pass