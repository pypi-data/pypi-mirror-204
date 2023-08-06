# 
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from dataclasses import asdict
from rich import print_json
from typer import Argument, Option, Typer
from typing import List, Tuple

from ..api import AccessMode, License, Predictor, PredictorStatus
from .auth import get_access_key
from .misc import create_learn_callback

app = Typer(no_args_is_help=True)

@app.command(name="retrieve", help="Retrieve a predictor.")
def retrieve_predictor (
    tag: str=Argument(..., help="Predictor tag.")
) -> None:
    predictor = Predictor.retrieve(tag, access_key=get_access_key())
    predictor = asdict(predictor) if predictor else None
    print_json(data=predictor)

@app.command(name="list", help="List available predictors.")
def list_predictors (
    mine: bool=Option(False, "--mine", help="Fetch only predictors owned by me."),
    status: PredictorStatus=Option(None, case_sensitive=False, help="Predictor status. This only applies when `--mine` is specified."),
    offset: int=Option(None, help="Pagination offset."),
    count: int=Option(None, help="Pagination count.")
) -> None:
    predictors = Predictor.list(mine=mine, status=status, offset=offset, count=count, access_key=get_access_key())
    predictors = [asdict(predictor) for predictor in predictors]
    print_json(data=predictors)

@app.command(name="search", help="Search predictors.")
def search_predictors (
    query: str=Argument(..., help="Search query."),
    offset: int=Option(None, help="Pagination offset."),
    count: int=Option(None, help="Pagination count.")
) -> None:
    predictors = Predictor.search(query=query, offset=offset, count=count, access_key=get_access_key())
    predictors = [asdict(predictor) for predictor in predictors]
    print_json(data=predictors)

@app.command(name="create", help="Create a predictor.")
def create_predictor (
    tag: str=Argument(..., help="Predictor tag."),
    description: str=Option("", help="Predictor description."),
    access: AccessMode=Option(AccessMode.Private, case_sensitive=False, help="Predictor access mode.")
) -> None:
    predictor = Predictor.create(tag, description=description, access=access, access_key=get_access_key())
    print_json(data=asdict(predictor))

@app.command(name="update", help="Update a predictor.")
def update_predictor (
    tag: str=Argument(..., help="Predictor tag."),
    description: str=Option(None, help="Predictor description."),
    access: AccessMode=Option(None, case_sensitive=False, help="Predictor access mode."),
    license: License=Option(None, case_sensitive=False, help="Predictor license."),
    topics: List[str]=Option(None, help="Predictor topics."),
    media: str=Option(None, help="Predictor media."),
    delete_media: bool=Option(False, "--delete-media", help="Delete existing media."),
) -> None:
    predictor = Predictor.update(
        tag,
        description=description,
        access=access,
        license=license,
        topics=topics,
        media=media,
        delete_media=delete_media,
        access_key=get_access_key()
    )
    print_json(data=asdict(predictor))

@app.command(name="delete", help="Delete a draft predictor.")
def delete_predictor (
    tag: str=Argument(..., help="Predictor tag.")
) -> None:
    result = Predictor.delete(tag, access_key=get_access_key())
    print_json(data=result)

@app.command(name="review", help="Review a draft predictor for any issues that might prevent it from being published.")
def review_predictor (
    tag: str=Argument(..., help="Predictor tag.")
) -> None:
    result = Predictor.review(tag, access_key=get_access_key())
    print_json(data=result)

@app.command(name="publish", help="Publish a draft predictor.")
def publish_predictor (
    tag: str=Argument(..., help="Predictor tag.")
) -> None:
    predictor = Predictor.publish(tag, access_key=get_access_key())
    print_json(data=asdict(predictor))

@app.command(name="archive", help="Archive a published predictor.")
def archive_predictor (
    tag: str=Argument(..., help="Predictor tag.")
) -> None:
    predictor = Predictor.archive(tag, access_key=get_access_key())
    print_json(data=asdict(predictor))

@app.callback()
def predictor_options (
    learn: bool = Option(None, "--learn", callback=create_learn_callback("https://docs.natml.ai/graph/predictors/type"), help="Learn about predictors in NatML.")
):
    pass