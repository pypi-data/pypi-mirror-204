#  -*- coding: utf-8 -*-
"""
Author: Dave Maddox
Refactored: Nikola Milojica
Notes:
- Formatted by black
"""

import datetime
import functools
import multiprocessing
import os

import click
import humanfriendly
import timeago
from pytablewriter import MarkdownTableWriter
from zenpy import Zenpy

multiprocessing.set_start_method("spawn", True)

ITEMS_EXCEPTION = "No call to Zendesk API were made, list of items is empty."
PRODUCTION = "env_prod"
SUPPORT = "technical_support"


def _ticket_status(text):
    return "Closed" if text == "Solved" else text


class ZendeskReportException(Exception):
    pass


class ZendeskReport:
    def __init__(self, email, organization, subdomain, token):
        self.client = Zenpy(email=email, subdomain=subdomain, token=token)
        self.items = None
        self.kind = None
        self.organization = organization

    def _create_header(self, current, _per_page):
        if self.kind == "tickets":
            return [
                f"Tickets {self._from_to(current, _per_page)}",
                "Priority",
                "Environment",
                "Request Type",
                "First Reply Time",
                "Created",
                "Updated",
                "Subject",
                "Status",
            ]

        if self.kind == "users":
            return [
                f"Users {self._from_to(current, _per_page)}",
                "Verified?",
                "Created",
                "Last Login",
            ]

    def _create_row(self, item):
        if self.kind == "tickets":
            return [
                f"[{item.id}](https://support.daon.com/tickets/{item.id})",
                item.priority.title(),
                "Production" if PRODUCTION in item.tags else "Non-Production",
                "Technical Support" if SUPPORT in item.tags else "Other",
                self._reply_time(item),
                item.created.strftime("%Y-%m-%d"),
                item.updated.strftime("%Y-%m-%d"),
                item.subject,
                _ticket_status(item.status.title()),
            ]

        if self.kind == "users":
            return [
                self._user_email(item),
                item.verified,
                item.created.strftime("%Y-%m-%d"),
                self._user_last_login(item),
            ]

    def _create_table(self, per_page):
        # TODO: consider writing proper writer Factory
        def _markdown_writer(headers):
            _writer = MarkdownTableWriter()
            _writer.headers = headers
            _writer.value_matrix = []
            return _writer

        if not self.items:
            raise ZendeskReportException(ITEMS_EXCEPTION)

        current = 1
        content = str()
        header = self._create_header(current, per_page)
        writer = _markdown_writer(header)
        for item in self.items:
            row = self._create_row(item)
            writer.value_matrix.append(row)
            current += 1
            if (current - 1) % per_page == 0 and current < len(self.items):
                content += writer.dumps() + "\n"
                header = self._create_header(current, per_page)
                writer = _markdown_writer(header)
        content += writer.dumps()
        self.items = None
        self.kind = None
        return content

    def _reply_time(self, ticket):
        time = self.client.tickets.metrics(ticket.id).reply_time_in_minutes["calendar"]
        if time:
            return humanfriendly.format_timespan(time * 60)
        return "None"

    def _from_to(self, current, _per_page):
        _from = current
        _to = min(current + _per_page - 1, len(self.items))
        _range = f"({_from} to {_to})"
        return _range

    @staticmethod
    def _user_email(user):
        return f"~~{user.email}~~" if user.suspended else user.email

    @staticmethod
    def _user_last_login(user):
        if user.last_login:
            now = datetime.datetime.now(datetime.timezone.utc)
            delta = now - user.last_login
            duration = timeago.format(user.last_login, now)
            if delta.days >= 90 and not user.suspended:
                return f"=={duration}=="
            return duration
        if not user.suspended:
            return "==Never=="
        return "Never"

    def tickets_table(
        self, update_window_days=30, end_date=datetime.datetime.now(), per_page=10,
    ):
        start_date = end_date - datetime.timedelta(days=update_window_days)
        self.kind = "tickets"
        self.items = list(
            self.client.search(
                organization=self.organization,
                updated_between=[start_date, end_date],
                type="ticket",
                order_by="priority",
                sort="desc",
            )
        )
        if len(self.items):
            return self._create_table(per_page)
        return "No tickets"

    def users_table(self, items_per_page=20):
        self.kind = "users"
        self.items = self.client.search(
            organization=self.organization, type="user", is_suspended="false",
        )
        if len(self.items):
            return self._create_table(items_per_page)
        return "No users"


if __name__ == "__main__":

    @click.group()
    def cli():
        """ Zendesk reporting tools command line interface. """

    def common_options(function):
        """ https://stackoverflow.com/questions/40182157 """
        options = [
            click.option(
                "--organization",
                "-o",
                envvar="ZEN_ORGANIZATION",
                help="Zendesk organisation.",
                required=True,
            ),
        ]
        return functools.reduce(lambda x, opt: opt(x), options, function)

    @cli.command()
    @click.option("--end", "-e", type=click.DateTime(), help="End date.")
    @click.option("--days", "-d", default=30, help="Time range in question.")
    @common_options
    def list_tickets(organization, days, end):
        """ List tickets for an organisation. """
        report = ZendeskReport(
            email=os.environ["ZEN_MAIL"],
            organization=organization,
            subdomain=os.environ["ZEN_SUBDOMAIN"],
            token=os.environ["ZEN_TOKEN"],
        )
        if not end:
            end = datetime.datetime.now()
        print(report.tickets_table(update_window_days=days, end_date=end))

    @cli.command()
    @common_options
    def list_users(organization):
        """ List users for an organisation. """
        report = ZendeskReport(
            email=os.environ["ZEN_MAIL"],
            organization=organization,
            subdomain=os.environ["ZEN_SUBDOMAIN"],
            token=os.environ["ZEN_TOKEN"],
        )
        print(report.users_table())

    cli()
