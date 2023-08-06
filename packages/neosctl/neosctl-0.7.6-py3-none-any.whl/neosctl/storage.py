import pathlib
import typing

import httpx
import typer

from neosctl import constant, util
from neosctl.auth import ensure_login
from neosctl.util import process_response

app = typer.Typer()

bucket_app = typer.Typer()
object_app = typer.Typer()
tagging_app = typer.Typer()

app.add_typer(bucket_app, name="bucket", help="Manage object buckets.")
app.add_typer(object_app, name="object", help="Manage objects.")
object_app.add_typer(tagging_app, name="tags", help="Manage object tags.")


def _storage_url(ctx: typer.Context, postfix: str) -> str:
    return "{}/{}".format(ctx.obj.storage_api_url.rstrip("/"), postfix)


def _load_statement(statement: typing.Optional[str], statement_filepath: typing.Optional[str]) -> str:
    if statement is not None:
        return statement

    if statement_filepath is not None:
        fp = util.get_file_location(statement_filepath or "")

        return fp.read_text()

    raise util.exit_with_output(
        msg="At least one of --statement/--statement-filepath is required.",
        exit_code=1,
    )


def _load_params(params_filepath: typing.Optional[str]) -> typing.Union[typing.List[typing.Any], None]:
    if params_filepath:
        fp = util.get_file_location(params_filepath)

        return util.load_fields_file(fp, "params")

    return None


def _handle(
    ctx: typer.Context,
    postfix: str,
    statement: typing.Optional[str] = None,
    statement_filepath: typing.Optional[str] = None,
    params_filepath: typing.Optional[str] = None,
) -> None:
    @ensure_login
    def _request(ctx: typer.Context, params: typing.Union[typing.List[typing.Any], None]) -> httpx.Response:
        return util.post(
            ctx,
            url=_storage_url(ctx, postfix),
            json={
                "statement": statement,
                "params": params,
            },
        )

    statement = _load_statement(statement, statement_filepath)
    params = _load_params(params_filepath)

    r = _request(ctx, params)
    process_response(r)


@app.command()
def execute(
    ctx: typer.Context,
    statement: typing.Optional[str] = typer.Option(
        None,
        "--statement",
        "-s",
        help="pSQL statement",
        callback=util.sanitize,
    ),
    statement_filepath: typing.Optional[str] = typer.Option(
        None,
        "--statement-filepath",
        "-sf",
        help="Filepath for statement sql file.",
        callback=util.sanitize,
    ),
    params_filepath: typing.Optional[str] = typer.Option(
        None,
        "--params-filepath",
        "-pf",
        help="Filepath for statement params json file.",
        callback=util.sanitize,
    ),
) -> None:
    """Execute a statement."""
    _handle(ctx, "execute", statement, statement_filepath, params_filepath)


@app.command()
def executemany(
    ctx: typer.Context,
    statement: typing.Optional[str] = typer.Option(
        None,
        "--statement",
        "-s",
        help="pSQL statement",
        callback=util.sanitize,
    ),
    statement_filepath: typing.Optional[str] = typer.Option(
        None,
        "--statement-filepath",
        "-sf",
        help="Filepath for statement sql file.",
        callback=util.sanitize,
    ),
    params_filepath: typing.Optional[str] = typer.Option(
        None,
        "--params-filepath",
        "-pf",
        help="Filepath for statement params json file.",
        callback=util.sanitize,
    ),
) -> None:
    """Execute a statement with multiple input params."""
    _handle(ctx, "executemany", statement, statement_filepath, params_filepath)


@app.command()
def fetch(
    ctx: typer.Context,
    statement: typing.Optional[str] = typer.Option(
        None,
        "--statement",
        "-s",
        help="pSQL statement",
        callback=util.sanitize,
    ),
    statement_filepath: typing.Optional[str] = typer.Option(
        None,
        "--statement-filepath",
        "-sf",
        help="Filepath for statement sql file.",
        callback=util.sanitize,
    ),
    params_filepath: typing.Optional[str] = typer.Option(
        None,
        "--params-filepath",
        "-pf",
        help="Filepath for statement params json file.",
        callback=util.sanitize,
    ),
) -> None:
    """Fetch results of a statement."""
    _handle(ctx, "fetch", statement, statement_filepath, params_filepath)


@app.command()
def fetchrow(
    ctx: typer.Context,
    statement: typing.Optional[str] = typer.Option(
        None,
        "--statement",
        "-s",
        help="pSQL statement",
        callback=util.sanitize,
    ),
    statement_filepath: typing.Optional[str] = typer.Option(
        None,
        "--statement-filepath",
        "-sf",
        help="Filepath for statement sql file.",
        callback=util.sanitize,
    ),
    params_filepath: typing.Optional[str] = typer.Option(
        None,
        "--params-filepath",
        "-pf",
        help="Filepath for statement params json file.",
        callback=util.sanitize,
    ),
) -> None:
    """Fetch first result of a statement."""
    _handle(ctx, "fetchrow", statement, statement_filepath, params_filepath)


@bucket_app.command(name="create")
def create_bucket(
    ctx: typer.Context,
    bucket_name: str = typer.Argument(
        ...,
        help="Bucket name",
        callback=util.validate_string_not_empty,
    ),
) -> None:
    """Create new bucket."""

    @ensure_login
    def _request(ctx: typer.Context, bucket_name: str) -> httpx.Response:
        return util.put(ctx, url=_storage_url(ctx, f"objects/{bucket_name}"))

    response = _request(ctx, bucket_name)
    process_response(response)


@bucket_app.command(name="list")
def list_buckets(ctx: typer.Context) -> None:
    """List buckets."""

    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.get(ctx, url=_storage_url(ctx, "objects"))

    response = _request(ctx)
    process_response(response)


@bucket_app.command(name="delete")
def delete_bucket(
    ctx: typer.Context,
    bucket_name: str = typer.Argument(
        ...,
        help="Bucket name",
        callback=util.validate_string_not_empty,
    ),
) -> None:
    """Delete bucket."""

    @ensure_login
    def _request(ctx: typer.Context, bucket_name: str) -> httpx.Response:
        return util.delete(ctx, url=_storage_url(ctx, f"objects/{bucket_name}"))

    response = _request(ctx, bucket_name)
    process_response(response)


@object_app.command(name="create")
def create_object(
    ctx: typer.Context,
    bucket_name: str = typer.Argument(
        ...,
        help="Bucket name",
        callback=util.validate_string_not_empty,
    ),
    object_name: str = typer.Argument(
        ...,
        help="Object name",
        callback=util.validate_string_not_empty,
    ),
    file: str = typer.Argument(
        ...,
        help="Path to the object file.",
        callback=util.validate_string_not_empty,
    ),
) -> None:
    """Create object."""

    @ensure_login
    def _request(ctx: typer.Context, bucket_name: str, object_name: str, file: str) -> httpx.Response:
        with pathlib.Path(file).open("rb") as fh:
            file_content = fh.read()

        return util.put(ctx, url=_storage_url(ctx, f"objects/{bucket_name}/{object_name}"), data=file_content)

    response = _request(ctx, bucket_name, object_name, file)
    process_response(response)


@object_app.command(name="list")
def list_objects(
    ctx: typer.Context,
    bucket_name: str = typer.Argument(
        ...,
        help="Bucket name",
        callback=util.validate_string_not_empty,
    ),
) -> None:
    """List objects."""

    @ensure_login
    def _request(ctx: typer.Context, bucket_name: str) -> httpx.Response:
        return util.get(ctx, url=_storage_url(ctx, f"objects/{bucket_name}"))

    response = _request(ctx, bucket_name)
    process_response(response)


@object_app.command(name="get")
def get_object(
    ctx: typer.Context,
    bucket_name: str = typer.Argument(
        ...,
        help="Bucket name",
        callback=util.validate_string_not_empty,
    ),
    object_name: str = typer.Argument(
        ...,
        help="Object name",
        callback=util.validate_string_not_empty,
    ),
    file: str = typer.Argument(
        ...,
        help="Path to file where to store the object.",
        callback=util.validate_string_not_empty,
    ),
) -> None:
    """Get object."""

    @ensure_login
    def _request(ctx: typer.Context, bucket_name: str, object_name: str) -> httpx.Response:
        return util.get(ctx, url=_storage_url(ctx, f"objects/{bucket_name}/{object_name}"))

    response = _request(ctx, bucket_name, object_name)
    if response.status_code >= constant.BAD_REQUEST_CODE:
        process_response(response)

    with pathlib.Path(file).open("wb") as fh:
        fh.write(response.content)


@object_app.command(name="delete")
def delete_object(
    ctx: typer.Context,
    bucket_name: str = typer.Argument(
        ...,
        help="Bucket name",
        callback=util.validate_string_not_empty,
    ),
    object_name: str = typer.Argument(
        ...,
        help="Object name",
        callback=util.validate_string_not_empty,
    ),
) -> None:
    """Delete object."""

    @ensure_login
    def _request(ctx: typer.Context, bucket_name: str, object_name: str) -> httpx.Response:
        return util.delete(ctx, url=_storage_url(ctx, f"objects/{bucket_name}/{object_name}"))

    response = _request(ctx, bucket_name, object_name)
    process_response(response)


@tagging_app.command(name="set")
def set_object_tags(
    ctx: typer.Context,
    bucket_name: str = typer.Argument(
        ...,
        help="Bucket name",
        callback=util.validate_string_not_empty,
    ),
    object_name: str = typer.Argument(
        ...,
        help="Object name",
        callback=util.validate_string_not_empty,
    ),
    tags: typing.List[str] = typer.Argument(
        ...,
        help="Tags as pairs of key=value",
        callback=util.validate_strings_are_not_empty,
    ),
) -> None:
    """Set object tags. Be aware that this command overwrites any tags that are already set to the object."""

    @ensure_login
    def _request(ctx: typer.Context, bucket_name: str, object_name: str, tags: typing.List[str]) -> httpx.Response:
        tags_list = []
        for tag in tags:
            key, value = tag.split("=", 1)
            tags_list.append({"key": key, "value": value})
        return util.put(
            ctx,
            url=_storage_url(ctx, f"objects/{bucket_name}/{object_name}?tagging"),
            json={"tags": tags_list},
        )

    response = _request(ctx, bucket_name, object_name, tags)
    process_response(response)


@tagging_app.command(name="get")
def get_object_tags(
    ctx: typer.Context,
    bucket_name: str = typer.Argument(
        ...,
        help="Bucket name",
        callback=util.validate_string_not_empty,
    ),
    object_name: str = typer.Argument(
        ...,
        help="Object name",
        callback=util.validate_string_not_empty,
    ),
) -> None:
    """Get object tags."""

    @ensure_login
    def _request(ctx: typer.Context, bucket_name: str, object_name: str) -> httpx.Response:
        return util.get(ctx, url=_storage_url(ctx, f"objects/{bucket_name}/{object_name}?tagging"))

    response = _request(ctx, bucket_name, object_name)
    process_response(response)


@tagging_app.command(name="delete")
def delete_object_tags(
    ctx: typer.Context,
    bucket_name: str = typer.Argument(
        ...,
        help="Bucket name",
        callback=util.validate_string_not_empty,
    ),
    object_name: str = typer.Argument(
        ...,
        help="Object name",
        callback=util.validate_string_not_empty,
    ),
) -> None:
    """Delete object tags."""

    @ensure_login
    def _request(ctx: typer.Context, bucket_name: str, object_name: str) -> httpx.Response:
        return util.delete(ctx, url=_storage_url(ctx, f"objects/{bucket_name}/{object_name}?tagging"))

    response = _request(ctx, bucket_name, object_name)
    process_response(response)
