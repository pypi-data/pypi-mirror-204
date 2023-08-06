from rfctl.awslocal import lambda_command
import click


@click.command()
@click.pass_context
def update_config_command(ctx: click.Context):
    funcdef = ctx.obj["funcdef"]
    click.echo("Updating config for function %s/%s" % (funcdef["metadata"]["namespace"], funcdef["metadata"]["name"]))
    lambda_args = ["update-function-configuration",
                   "--function-name", funcdef["metadata"]["name"],
                   "--handler", funcdef["spec"]["handler"],
                   "--runtime", funcdef["spec"]["runtime"],
                   "--timeout", funcdef["spec"]["timeout"]]
    lambda_command(ctx.obj["endpoint"], lambda_args)
