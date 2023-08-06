from rfctl.awslocal import lambda_command
import click


@click.command()
@click.pass_context
def create_url_command(ctx: click.Context):
    funcdef = ctx.obj["funcdef"]
    click.echo("Creating url for function %s/%s" % (funcdef["metadata"]["namespace"], funcdef["metadata"]["name"]))
    lambda_args = ["create-function-url-config",
                   "--function-name", funcdef["metadata"]["name"],
                   "--auth-type", "None"]
    lambda_command(ctx.obj["endpoint"], lambda_args)
