#  -*- coding: utf-8 -*-
"""
Author: Nikola Milojica
Notes:
- Formatted by black
- Imports optimized by isort
"""

import datetime
import functools
from copy import copy

import click
import requests
from furl import furl


ADMINISTRATIVE_RULES = b"Request forbidden by administrative rules."
ADMINISTRATIVE_RULES_HTML = """<html><body><h1>403 Forbidden</h1>
Request forbidden by administrative rules.
</body></html>"""


class GrafanaReportException(Exception):
    pass


class GrafanaReport:
    def __init__(self, dashboard, organization, password, username, production=True):
        self.dashboard = dashboard
        self.default_arguments = {"orgId": 1}
        self.domain = "https://grafana.trustx.com/"
        self.endpoints = {"render": ["render", "d-solo"]}
        self.frame = {
            "height": 500,
            "theme": "light",
            "tz": "Europe/Dublin",
            "width": 1000,
        }
        self.production = production
        self.organization = organization
        self.panels = {
            "authentications": 6,
            "users": 2,
        }
        self.password = password
        self.username = username

    def __call__(self, days=30, *args, **kwargs):
        _from, _to = self.from_to_range(days=days)
        args = self._prepare_arguments(_from, _to)
        url = self._prepare_url()
        self._graph(args, "authentications", url)
        self._graph(args, "users", url)

    def _prepare_arguments(self, _from, _to):
        args = {}
        args.update(self.frame)
        args.update(self.default_arguments)
        args.update({"from": _from, "to": _to})
        return args

    def _prepare_url(self):
        url = furl(self.domain)
        path = copy(self.endpoints["render"])
        path.extend([self.dashboard, self.organization])
        url.path.set(path)
        return url

    def _graph(self, args, scope, url, path=None):
        if scope not in self.panels:
            raise GrafanaReportException(
                f"Current scope is not supported, please choose one of the following {self.panels}."
            )
        args.update({"panelId": self.panels[scope]})
        url.set(args=args)
        if not path:
            if not self.production:
                file = f"./grafana-{scope}.jpg"
            else:
                file = f"./docs/images/grafana-{scope}.jpg"
        else:
            file = path
        response = requests.get(url.url, auth=(self.username, self.password))
        if not isinstance(response.content, bytes):
            raise GrafanaReportException(response.content)
        response.raise_for_status()

        with open(file, "wb") as f:
            f.write(response.content)

    @staticmethod
    def from_to_range(days):
        _to = int(datetime.datetime.now().strftime("%s")) * 1000
        _from = (
            int((datetime.datetime.now() + datetime.timedelta(-days)).strftime("%s"))
            * 1000
        )
        return _from, _to

    graph = _graph
    prepare_arguments = _prepare_arguments
    prepare_url = _prepare_url


if __name__ == "__main__":

    @click.group()
    def cli():
        """ Grafana reporting tools command line interface. """

    def common_options(function):
        """ https://stackoverflow.com/questions/40182157 """
        options = [
            click.option(
                "--board",
                "-b",
                envvar="GRAF_DASHBOARD",
                help="Dashboard ID.",
                required=True,
            ),
            click.option("--days", "-d", default=30, help="Time range in question."),
            click.option(
                "--file-path",
                "-f",
                envvar="GRAF_FILE",
                help="File output path.",
                default=None,
            ),
            click.option(
                "--organization",
                "-o",
                envvar="GRAF_ORGANIZATION",
                help="Grafana organizations id.",
                required=True,
            ),
            click.option(
                "--password",
                "-p",
                envvar="GRAF_PASSWORD",
                help="Grafana user's password.",
                required=True,
            ),
            click.option(
                "--username",
                "-u",
                envvar="GRAF_USER",
                help="Grafana user's name.",
                required=True,
            ),
        ]
        return functools.reduce(lambda x, opt: opt(x), options, function)

    @cli.command()
    @common_options
    def authentications(board, days, file_path, organization, password, username):
        integration = GrafanaReport(board, organization, password, username, production=False)
        _from, _to = integration.from_to_range(days=days)
        integration.graph(
            integration.prepare_arguments(_from, _to),
            "authentications",
            integration.prepare_url(),
            path=file_path,
        )

    @cli.command()
    @common_options
    def users(board, days, file_path, organization, password, username):
        integration = GrafanaReport(board, organization, password, username, production=False)
        _from, _to = integration.from_to_range(days=days)
        integration.graph(
            integration.prepare_arguments(_from, _to),
            "users",
            integration.prepare_url(),
            path=file_path,
        )

    cli()
