#  -*- coding: utf-8 -*-
"""
Author: Nikola Milojica
Notes:
- Formatted by black
- Imports optimized by isort
"""

import json
import os

import psutil
import pytest
import responses

from macros.reports.pingdom import PingdomIntegration, PingdomReport

# load responses with endpoints and json data
with open("tests/data/pingdom", "r") as f:
    for line in f.readlines():
        data = json.loads(line)
        for key, value in data.items():
            responses.add(
                responses.GET, key, json=value, status=200,
            )
CREDENTIALS = {
    "apikey": "test",
    "email": "test",
    "organization": "test",
    "password": "test",
    "username": "test",
}
FILE_UPTIME = "pingdom_uptime.png"
FILE_RESPONSE = "pingdom_response.png"
FILE_RESPONSE_COUNTRY = "pingdom_response_country.png"
PATH_DATA = "tests/data/{}"
PATH_PROCESSED = "tests/processed/{}"

with open("tests/data/pingdom.json", "r") as f:
    REFERENCE_BLOB = json.load(f)

REFERENCE_HTML = """<div id="summary">
            <div class="leftTopRounded"></div>
            <div class="leftBottomRounded"></div>
            <div class="rightTopRounded"></div>
            <div class="rightBottomRounded"></div>
            <div id="columnOne">
                <div id="lastChecked">
                    <div id="statusIcon" class="up"></div>
                    <h3>Last checked</h3>
                    <p>12/17/2019, 10:29:49</p>
                </div>
            </div>
            <div id="columnTwo">
                <h3>Uptime this month</h3>
                <p class="large">99.9%</p>
            </div>
            <div id="columnThree">
                <h3>Avg. resp. time this month</h3>
                <p class="large">231 ms</p>
            </div>
            <div id="columnFour">
                <p class="top"><strong>Check type:</strong> HTTP</p>
                <p><strong>Check resolution:</strong> 1 minutes</p>
            </div>
        </div>
        """  # TODO: load from file

ZIPPED_RANGES = [
    ("2019-11-16", "2019-11-17"),
    ("2019-11-17", "2019-11-18"),
    ("2019-11-18", "2019-11-19"),
    ("2019-11-19", "2019-11-20"),
    ("2019-11-20", "2019-11-21"),
    ("2019-11-21", "2019-11-22"),
    ("2019-11-22", "2019-11-23"),
    ("2019-11-23", "2019-11-24"),
    ("2019-11-24", "2019-11-25"),
    ("2019-11-25", "2019-11-26"),
    ("2019-11-26", "2019-11-27"),
    ("2019-11-27", "2019-11-28"),
    ("2019-11-28", "2019-11-29"),
    ("2019-11-29", "2019-11-30"),
    ("2019-11-30", "2019-12-01"),
    ("2019-12-01", "2019-12-02"),
    ("2019-12-02", "2019-12-03"),
    ("2019-12-03", "2019-12-04"),
    ("2019-12-04", "2019-12-05"),
    ("2019-12-05", "2019-12-06"),
    ("2019-12-06", "2019-12-07"),
    ("2019-12-07", "2019-12-08"),
    ("2019-12-08", "2019-12-09"),
    ("2019-12-09", "2019-12-10"),
    ("2019-12-10", "2019-12-11"),
    ("2019-12-11", "2019-12-12"),
    ("2019-12-12", "2019-12-13"),
    ("2019-12-13", "2019-12-14"),
    ("2019-12-14", "2019-12-15"),
    ("2019-12-15", "2019-12-16"),
    ("2019-12-16", "2019-12-17"),
]

integration = PingdomIntegration(**CREDENTIALS)
report = PingdomReport(REFERENCE_BLOB)


@responses.activate
def test_integration():
    """ Test end result of __call__() with mocked GET requests. """
    blob = {
        "aro": integration.average_response_for_organization(
            _from="2019-11-16", _to="2019-12-16"
        ),
        "gco": integration.general_check_for_organization(),
        "pco": integration._fetch_daily_performances(ZIPPED_RANGES),
    }
    assert blob == REFERENCE_BLOB


def test_report():
    """ Test report images and HTML. """
    if 9091 not in [i.laddr.port for i in psutil.net_connections()]:
        pytest.skip("No ORCA Docker container found on default port 9091.")
    html = report.create_banner()
    assert html == REFERENCE_HTML
    assert (
        open(PATH_DATA.format(FILE_RESPONSE), "rb").read()
        == open(PATH_PROCESSED.format(FILE_RESPONSE), "rb").read()
    )
    assert (
        open(PATH_DATA.format(FILE_RESPONSE_COUNTRY), "rb").read()
        == open(PATH_PROCESSED.format(FILE_RESPONSE_COUNTRY), "rb").read()
    )
    assert (
        open(PATH_DATA.format(FILE_UPTIME), "rb").read()
        == open(PATH_PROCESSED.format(FILE_UPTIME), "rb").read()
    )


def setup_module():
    report.create_response_time_plot(path=PATH_PROCESSED.format(FILE_RESPONSE))
    report.create_response_time_plot_per_country(
        path=PATH_PROCESSED.format(FILE_RESPONSE_COUNTRY)
    )
    report.create_up_time_plot(path=PATH_PROCESSED.format(FILE_UPTIME))


def teardown_module():
    destination_folder = "tests/processed/"
    files = os.listdir(destination_folder)
    for file in files:
        if file.startswith("pingdom"):
            os.remove(os.path.join(destination_folder, file))
