#  -*- coding: utf-8 -*-
"""
Author: Nikola Milojica
Notes:
- Formatted by black
- Imports optimized by isort
"""

import json
import re

import responses

from macros.reports.zendesk import ZendeskReport

CREDENTIALS = {
    "email": "test",
    "organization": "test",
    "subdomain": "test",
    "token": "test",
}


def setup_client_and_responses():
    with open("tests/data/zendesk", "r") as f:
        response_data = []
        for line in f.readlines():
            response_data.append(json.loads(line))

    urls = [
        re.compile(
            r"https://test\.zendesk\.com/api/v2/search\.json\?query=organization:test"
            r"%20type:ticket%20order_by:priority%20sort:desc%20updated%3E.*%20updated%3C.*"
        ),
        "https://test.zendesk.com/api/v2/search.json?query=organization:test type:user is_suspended:false",
        "https://test.zendesk.com/api/v2/tickets/33881/metrics.json",
        "https://test.zendesk.com/api/v2/tickets/33892/metrics.json",
        "https://test.zendesk.com/api/v2/tickets/33742/metrics.json",
        "https://test.zendesk.com/api/v2/tickets/34649/metrics.json",
        "https://test.zendesk.com/api/v2/tickets/34427/metrics.json",
        "https://test.zendesk.com/api/v2/tickets/33739/metrics.json",
    ]

    for response, url in zip(response_data, urls):
        responses.add(
            responses.GET, url, json=response, status=200,
        )
    return ZendeskReport(**CREDENTIALS)


@responses.activate
def test_tickets_table():
    report = setup_client_and_responses()
    with open("tests/data/zendesk_tickets.txt", "r") as f:
        assert f.read() == report.tickets_table()


@responses.activate
def test_users_table():
    report = setup_client_and_responses()
    actual_table = report.users_table().split("\n")
    with open("tests/data/zendesk_users.txt", "r") as f:
        reference_table = f.read().split("\n")
    # direct comparision to reference table is not possible since column "created"
    # is calculating how much days ago it was, this test is flawed but sufficient
    for row_actual, row_reference in zip(actual_table[:-1], reference_table[:-1]):
        row_actual_parts = row_actual.split("|")[1:-1]
        row_reference_parts = row_reference.split("|")[1:-1]
        for index in (0, 1, 2):
            assert row_actual_parts[index] == row_reference_parts[index]
