import http

import click

import time

from .api import delete_chart_version


def get_name_and_versions_to_delete(chart_response, keep=2):
    """
    Get name and unused versions from chart api response. Please see test if confusing about the input and output.
    If less than 1 to keep, return empty empty to delete
    :param chart_response: api response of charts
    :param keep: number of versions to keep. default only keep one
    :return: Dict(str, list) contains chart name and versions
    """
    name_and_versions = dict()

    if keep < 1:
        return name_and_versions

    for k, v in chart_response.items():
        name_and_versions[k] = list()
        count = 0

        for value in v:
            if count >= keep:
                name_and_versions[k].append(value['version'])
            else:
                count += 1
    return name_and_versions

def calculate_unique_charts(name_and_versions, sleep_seconds):
    """
    Call the endpoint to explain sleep delay for total charts
    :param name_and_versions: Dict(str, list) which stores chart name and its versions in list
    :return:
    """
    unique_charts = 0
    for name, versions in name_and_versions.items():
        for version in versions:
            unique_charts += 1
    total_sleep_delay = sleep_seconds * unique_charts
    click.echo(f'Will sleep for {total_sleep_delay} seconds during deletion of {unique_charts} charts.')
    return unique_charts


def delete_name_and_versions(name_and_versions, sleep_seconds, unique_charts):
    """
    Call the endpoint to delete unused charts
    :param name_and_versions: Dict(str, list) which stores chart name and its versions in list
    :return:
    """
    index = 0
    for name, versions in name_and_versions.items():
        for version in versions:
            index += 1
            click.echo(f'Will remove chart: {name}, version: {version}')
            resp = delete_chart_version(name, version)

            if resp.status_code == http.HTTPStatus.OK:
                click.echo(f'Removed chart: {name}, version: {version}, index: {index}/{unique_charts}')
            else:
                click.echo(f"Fail to delete chart: {name}, version: {version}, "
                           f"status: {resp.status_code}, reason: {resp.reason}", color='red')
            time.sleep(sleep_seconds)
