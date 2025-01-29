import click
from k8s import get_cluster_health

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """KubeSage - AI-Powered Kubernetes Troubleshooting Tool"""
    pass


@cli.command()  # ✅ This correctly registers the command
def check_health():
    """Check cluster health using Kubernetes API"""
    get_cluster_health()


if __name__ == "__main__":
    cli()  # ✅ Make sure you are calling `cli()`
