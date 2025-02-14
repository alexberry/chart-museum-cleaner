import click

from .api import list_all_charts
from .cleaner import get_name_and_versions_to_delete, delete_name_and_versions, calculate_unique_charts

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command()
@click.option('--keep', default=2, help='Number of recent versions to keep and not delete', show_default=True, type=int)
@click.option('--sleep-seconds', default=0, help='Number of seconds to sleep between delete calls. Useful if bucket backends return rate limit errors on large cleanups.', show_default=True, type=float)
def delete(keep, sleep_seconds):
    """
    Clean up chart versions and keep number of newer versions
    :param keep: number of versions to keep
    :return:
    """
    if keep < 1:
        click.echo("--keep should be greater than 1. Do you really want to remove all charts?")
        return

    response = list_all_charts()
    name_and_versions_to_delete = get_name_and_versions_to_delete(response, keep)
    unique_charts = calculate_unique_charts(name_and_versions_to_delete, sleep_seconds)
    delete_name_and_versions(name_and_versions_to_delete, sleep_seconds, unique_charts)


def main():
    cli()
