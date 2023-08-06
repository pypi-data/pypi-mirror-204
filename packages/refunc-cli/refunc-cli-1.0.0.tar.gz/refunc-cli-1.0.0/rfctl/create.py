from rfctl.awslocal import lambda_command
from rfctl.build import do_build
import click
import os


@click.command()
@click.pass_context
def create_command(ctx: click.Context):
    funcdef = ctx.obj["funcdef"]
    out = os.path.join(ctx.obj["working_dir"], "lambda.zip")
    do_build(ctx, out)
    click.echo("Creating function %s/%s" % (funcdef["metadata"]["namespace"], funcdef["metadata"]["name"]))
    lambda_args = ["create-function",
                   "--function-name", funcdef["metadata"]["name"],
                   "--handler", funcdef["spec"]["handler"],
                   "--zip-file", "fileb://{}".format(out),
                   "--runtime", funcdef["spec"]["runtime"],
                   "--timeout", funcdef["spec"]["timeout"]]
    lambda_command(ctx.obj["endpoint"], lambda_args)
