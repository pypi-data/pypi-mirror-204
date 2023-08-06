from rfctl.schema import funcdef_schema, set_funcdef_defaults
from rfctl.build import build_command
from rfctl.create import create_command
from rfctl.delete import delete_command
from rfctl.get import get_command
from rfctl.update_code import update_code_command
from rfctl.update_config import update_config_command
from rfctl.create_url import create_url_command
from rfctl.delete_url import delete_url_command
from rfctl.get_url import get_url_command
import jsonschema
import click
import yaml
import os


@click.group()
@click.option('--endpoint', default=os.environ.get("AWS_DEFAULT_ENDPOINT", ""))
@click.option('--manifest', default="lambda.yaml", type=click.Path(exists=True, dir_okay=False, resolve_path=True))
@click.pass_context
def cli(ctx: click.Context, endpoint, manifest):
    click.echo("Function manifest founding in %s" % manifest)
    ctx.obj, funcdef = {"working_dir": os.getcwd()}, {}
    validate_error = None
    with open(manifest, 'r', encoding="utf-8") as fd:
        funcdef = yaml.load(fd, Loader=yaml.FullLoader)
        validate_error = None
    try:
        jsonschema.validate(instance=funcdef, schema=funcdef_schema)
    except Exception as e:
        validate_error = "{}".format(e).split("\n", maxsplit=1)[0].strip()
    if not validate_error is None:
        click.echo("Function manifest error %s" % validate_error)
        exit(-1)
    if not endpoint:
        click.echo("Endpoint can't be empty")
        exit(-1)
    os.chdir(os.path.dirname(manifest))
    os.environ.update({
        "AWS_DEFAULT_REGION": funcdef["metadata"]["namespace"]
    })
    ctx.obj["endpoint"] = endpoint
    ctx.obj["funcdef"] = set_funcdef_defaults(funcdef)


cli.add_command(build_command, "build")
cli.add_command(create_command, "create")
cli.add_command(delete_command, "delete")
cli.add_command(get_command, "get")
cli.add_command(update_code_command, "update-code")
cli.add_command(update_config_command, "update-config")
cli.add_command(create_url_command, "create-url")
cli.add_command(delete_url_command, "delete-url")
cli.add_command(get_url_command, "get-url")

if __name__ == "__main__":
    cli({}, *(), **{})
