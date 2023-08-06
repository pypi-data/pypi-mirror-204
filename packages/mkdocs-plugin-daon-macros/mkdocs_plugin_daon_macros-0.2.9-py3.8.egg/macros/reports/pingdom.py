#  -*- coding: utf-8 -*-
"""
Author: Nikola Milojica
Notes:
- Formatted by black
- Imports optimized by isort
"""

import datetime
import functools
import io
import json
import os
import statistics
import time
from abc import ABC

import click
import iso3166
import plotly
import plotly.graph_objects as go
import requests
from _plotly_utils.utils import PlotlyJSONEncoder
from dateutil.relativedelta import relativedelta
from furl import furl
from PIL import Image
from pycountry_convert import country_alpha2_to_continent_code as a2_to_continent
from requests.auth import HTTPBasicAuth


class AbstractPingdomIntegration(ABC):
    """ Abstract Class for Pingdom Integration. """


class AbtractPingdomReport(ABC):
    """ Abstract Class for Pingdom Report. """


class PingdomIntegrationException(Exception):
    """ Basic exception for Pingdom Report class. """


class PingdomIntegration(AbstractPingdomIntegration):
    """ Pingdom Integration Class. """

    def __init__(self, apikey, email, password, username, organization=None):
        self._credentials = {
            "apikey": apikey,
            "email": email,
            "password": password,
            "username": username,
        }
        self.auth = HTTPBasicAuth(
            self._credentials["username"], self._credentials["password"]
        )
        self.endpoints = {
            "average_response_time": "https://api.pingdom.com/api/2.0/summary.average/",
            "daily_performance": "https://api.pingdom.com/api/2.1/summary.performance/",
            "general_check": "https://api.pingdom.com/api/2.0/checks/",
        }
        self.headers = {
            "App-Key": self._credentials["apikey"],
            "Account-Email": self._credentials["email"],
        }
        self.kwarg_param_map = {
            "by_country": {"bycountry": "true"},
            "up_time": {"includeuptime": "true"},
        }
        self.organization = organization

    def __call__(self, *args, **kwargs):
        """ Method used to call data for specific organization's check id. """
        if not self.organization:
            raise PingdomIntegrationException(
                "Organization value is missing. You may assign one directly to this "
                "instance e.g. instance.organization = 'value' if you plan to use __call__()."
            )
        period = {
            "from_datetime": datetime.datetime.utcnow() - relativedelta(days=31),
            "to_datetime": datetime.datetime.utcnow() - relativedelta(days=1),
        }
        period.update(
            {
                "from_string": period["from_datetime"].date().__str__(),
                "to_string": period["to_datetime"].date().__str__(),
            }
        )
        from_list = [
            (period["from_datetime"] + datetime.timedelta(days=day))
            .date()
            .__str__()
            for day in range(31)
        ]
        to_list = [
            (period["from_datetime"] + datetime.timedelta(days=day + 1))
            .date()
            .__str__()
            for day in range(31)
        ]
        zipped_ranges = zip(from_list, to_list)
        aro = self.average_response_for_organization(
            _from=period["from_string"], _to=period["to_string"],
        )
        gco = self.general_check_for_organization()
        pco_list = self._fetch_daily_performances(zipped_ranges)
        blob = {
            "aro": aro,
            "gco": gco,
            "pco": pco_list,
        }
        return blob

    def _api_call(self, endpoint, data=None, organization=None, *args, **kwargs):
        """
        Main wrapper around requests library.
        :param endpoint: str: endpoint to be used to fetch data
        :param data: dict: body of POST request
        :param organization: str: organization Pingdom check id
        :param args: *args
        :param kwargs: **kwargs
        :return: dictionary JSON representation fetched from endpoint
        """

        def get_parameters_from_kwargs(_kwargs):
            """
            Method that build parameters dictionary from kwargs.
            :param _kwargs: keywords arguments
            :return: dict
            """
            parameters = {"params": {}}
            for key, value in self.kwarg_param_map.items():
                if key in _kwargs:
                    if _kwargs[key]:
                        parameters["params"].update(value)
            _from = None
            _to = None
            if "_from" in _kwargs and "_to" in _kwargs:
                try:
                    _from = datetime.datetime.strptime(_kwargs["_from"], "%Y-%m-%d")
                    _to = datetime.datetime.strptime(_kwargs["_to"], "%Y-%m-%d")
                except ValueError as e:
                    raise PingdomIntegrationException(
                        f"Wrong datetime value or format. Expecting ISO 8601 value "
                        f"(%Y-%m-%d), but got {_kwargs['from']} and {_kwargs['to']} "
                        f"instead.\n"
                        f"Datetime error message: {e}"
                    )
            else:
                # TODO: add offset
                time_range = {}
                for key_word in ("years", "months", "week", "days", "hours", "seconds"):
                    if key_word in kwargs:
                        time_range[key_word] = kwargs[key_word]
                if time_range:
                    _from = datetime.datetime.now() - relativedelta(**time_range)
                    _to = datetime.datetime.now()
            if _from and _to:
                _from = time.mktime(_from.timetuple())
                _to = time.mktime(_to.timetuple())
                parameters["params"].update({"from": _from, "to": _to})
            return parameters

        arguments = {
            "auth": self.auth,
            "headers": self.headers,
        }
        params = get_parameters_from_kwargs(kwargs)
        url = furl(self.endpoints[endpoint])
        if organization:
            url.path.add(organization)
        if params["params"]:
            arguments.update(params)
        if not data:
            response = requests.get(url.url, **arguments)
        else:
            arguments.update({"data": data})
            response = requests.post(url.url, **arguments)
        return response.json()

    def _fetch_daily_performances(self, zipped_ranges):
        """
        Perform performance_for_organization() on list of date ranges.
        :param zipped_ranges: list of tuples: dates as yyyy-mm-dd format
        :return: list
        """
        pco_list = []
        for _range in zipped_ranges:
            data = self.performance_for_organization(_from=_range[0], _to=_range[1])
            data["summary"]["hours"] = data["summary"]["hours"][:-1]
            hourly_response = []
            for index, item in enumerate(data["summary"]["hours"]):
                hour = index.__str__().rjust(2, "0") + ":00"
                item.update({"hour": hour})
                hourly_response.append(item["avgresponse"])
            if hourly_response:
                average_response = statistics.mean(hourly_response)
            else:
                average_response = None
            pco_list.append(
                {"average_response": average_response, "data": data, "date": _range[0]}
            )
        return pco_list

    def average_response_for_organization(
        self, by_country=True, organization=None, up_time=True, *args, **kwargs
    ):
        """
        Request average response time for organizations with check id.
        :param organization: str: organization check id
        :param by_country: bool: group by country, default True
        :param up_time: bool, group by up time, default True
        :param args: *args
        :param kwargs: **kwargs
        :return: dict
        """
        if not organization:
            if not self.organization:
                raise PingdomIntegrationException(
                    "No customer/organization provided, neither in __init__() or "
                    "in the average_response_for_organization()."
                )  # TODO: go DRY
            organization = self.organization
        if by_country:
            kwargs.update({"by_country": True})
        if up_time:
            kwargs.update({"up_time": True})
        response = self._api_call(
            "average_response_time", organization=organization, *args, **kwargs
        )
        return response

    def general_check_for_organization(self, organization=None, *args, **kwargs):
        """
        Request general check for organization with check id.
        :param organization: str: organization check id
        :param args: *args
        :param kwargs: **kwargs
        :return: dict
        """
        if not organization:
            if not self.organization:
                raise PingdomIntegrationException(
                    "No customer/organization provided, neither in __init__() or "
                    "in the general_check_for_organization()."
                )  # TODO: go DRY
            organization = self.organization
        response = self._api_call(
            "general_check", organization=organization, *args, **kwargs
        )
        return response

    def performance_for_organization(
        self, organization=None, up_time=True, *args, **kwargs
    ):
        """
        Request performance metrics for organization with check id.
        :param organization: str: organization check id
        :param up_time: bool, group by up time, default True
        :param args: *args
        :param kwargs: **kwargs
        :return: dict
        """
        if not organization:
            if not self.organization:
                raise PingdomIntegrationException(
                    "No customer/organization provided, neither in __init__() or "
                    "in the performance_for_organization()."
                )  # TODO: go DRY
            organization = self.organization
        if up_time:
            kwargs.update({"up_time": True})
        response = self._api_call(
            "daily_performance", organization=organization, *args, **kwargs
        )
        return response


class PingdomReport(AbtractPingdomReport):
    """ Pingdom Report Class. """

    def __init__(self, blob=None, docker=True, mock=False):
        if mock:
            with open("./test_data/pingdom.json", "r") as f:
                blob = json.load(f)
        # TODO: raise exception
        self.__dict__.update(blob)
        self.continent_map = {
            "AF": "africa",
            "AS": "asia",
            "EU": "europe",
            "NA": "north america",
            "SA": "south america",
        }
        if isinstance(docker, bool):
            self.docker = docker
        else:
            self.docker = False
        self.mock = mock
        if not self.docker:
            try:
                plotly.io.orca.config.executable = os.environ["ORCA"]
                plotly.io.orca.config.save()
            except KeyError:
                raise  # TODO: PingdomReportException

    @staticmethod
    def _save_with_orca_docker(
        figure, file_path, _format="png", height=0, port=9091, scale=1, width=0
    ):
        """
        Method for saving images with ORCA docker container (default port 9091).
        """
        if height == 0 and width == 0:
            raise ValueError  # TODO: PingdomReportException
        orca_url = f"http://localhost:{port}/"
        params = {
            "figure": figure.to_dict(),
            "format": _format,
            "height": height,
            "scale": scale,
            "width": width,
        }
        data = json.dumps(params, cls=PlotlyJSONEncoder)
        response = requests.post(orca_url, data=data)
        image = response.content
        with open(file_path, "wb") as f:
            Image.open(io.BytesIO(image)).save(f)

    def create_banner(self):
        """
        Method for creating Pingdom banner. Transforms REST API data into HTML string.
        """
        _up_time = self.aro["summary"]["status"]["totalup"] / sum(
            [value for value in self.aro["summary"]["status"].values()]
        )
        _last_check = datetime.datetime.fromtimestamp(self.gco["check"]["lasttesttime"])
        data = {
            "average_response_time": statistics.mean(
                [
                    i["avgresponse"]
                    for i in self.aro["summary"]["responsetime"]["avgresponse"]
                ]
            ),
            "check_resolution": self.gco["check"]["resolution"],
            "check_type": [_type for _type in self.gco["check"]["type"]][0].upper(),
            "last_check": _last_check.strftime("%m/%d/%Y, %H:%M:%S"),
            "status": self.gco["check"]["status"],
            "up_time": f"{'{:2.1f}%'.format(_up_time * 100)}",
        }
        html = """<div id="summary">
            <div class="leftTopRounded"></div>
            <div class="leftBottomRounded"></div>
            <div class="rightTopRounded"></div>
            <div class="rightBottomRounded"></div>
            <div id="columnOne">
                <div id="lastChecked">
                    <div id="statusIcon" class="{status}"></div>
                    <h3>Last checked</h3>
                    <p>{last_check}</p>
                </div>
            </div>
            <div id="columnTwo">
                <h3>Uptime this month</h3>
                <p class="large">{up_time}</p>
            </div>
            <div id="columnThree">
                <h3>Avg. resp. time this month</h3>
                <p class="large">{average_response_time} ms</p>
            </div>
            <div id="columnFour">
                <p class="top"><strong>Check type:</strong> {check_type}</p>
                <p><strong>Check resolution:</strong> {check_resolution} minutes</p>
            </div>
        </div>
        """.format(
            **data
        )
        return html

    def create_up_time_plot(self, height=400, path=None, width=1200):
        """
        Method for creating up time and outages plot per country png file. If not self.mock, it will show figure in your
        browser. Otherwise (in production) it will save image into Mkdocs root folder under /docs/images/.
        """
        _outages = 0
        hours = []
        down_time = []
        unmonitored_time = []
        up_time = []
        for i in self.pco:
            if i["average_response"] != "None":
                for j in i["data"]["summary"]["hours"]:
                    hour = "{} {}".format(i["date"], j["hour"])
                    hours.append(hour)
                    down_time.append(j["downtime"])
                    unmonitored_time.append(j["unmonitored"])
                    up_time.append(j["uptime"])
                    if j["downtime"] > 0:
                        _outages += 1
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hours, y=down_time, name="Down Time"))
        fig.add_trace(go.Scatter(x=hours, y=unmonitored_time, name="Unmonitored Time"))
        fig.add_trace(go.Scatter(x=hours, y=up_time, name="Up Time"))
        fig.update_layout(
            height=height,
            width=width,
            xaxis_title="Date",
            yaxis_title="Seconds per day",
        )
        if path:
            file_path = path
        else:
            file_path = "./docs/images/pingdom_uptime.png" if not self.mock else "./pingdom_uptime.png"
        if self.docker:
            self._save_with_orca_docker(fig, file_path, height=height, width=width)
        else:
            fig.write_image(file_path)
        if self.mock:
            fig.show()

    def create_response_time_plot(self, height=400, path=None, width=1200):
        """
        Method for creating response time plot png file. If not self.mock, it will show figure in your browser.
        Otherwise (in production) it will save image into Mkdocs root folder under /docs/images/.
        """
        dates = [datetime.datetime.strptime(i["date"], "%Y-%m-%d") for i in self.pco]
        responses = []
        for i in self.pco:
            appendix = None
            if (
                i["average_response"] != "None" and i["average_response"]
            ):  # TODO: debug this
                appendix = round(float(i["average_response"]), 1)
            responses.append(appendix)
        fig = go.Figure(data=[go.Scatter(x=dates, y=responses)])
        fig.update_layout(
            height=height, width=width, xaxis_title="Date", yaxis_title="Milliseconds",
        )
        if path:
            file_path = path
        else:
            file_path = (
                "./docs/images/pingdom_response.png"
                if not self.mock
                else "./pingdom_response.png"
            )
        if self.docker:
            self._save_with_orca_docker(fig, file_path, height=height, width=width)
        else:
            fig.write_image(file_path)
        if self.mock:
            fig.show()

    def create_response_time_plot_per_country(self, height=800, path=None, width=1200):
        """
        Method for creating response time plot per country png file. If not self.mock, it will show figure in your
        browser. Otherwise (in production) it will save image into Mkdocs root folder under /docs/images/.
        """
        response_list = self.aro["summary"]["responsetime"]["avgresponse"]
        data = {
            "continents": list(
                set([a2_to_continent(i["countryiso"]) for i in response_list])
            ),
            "locations": [
                iso3166.countries.get(i["countryiso"]).alpha3 for i in response_list
            ],
            "milliseconds": [i["avgresponse"] for i in response_list],
        }
        fig = go.Figure(
            data=go.Choropleth(
                autocolorscale=False,
                colorbar_title="Milliseconds",
                colorscale="greens",
                locations=data["locations"],
                locationmode="ISO-3",
                marker_line_color="black",
                marker_line_width=1,
                reversescale=True,
                z=data["milliseconds"],
            )
        )
        fig.update_layout(
            geo=dict(
                projection_type="miller",
                scope=self.continent_map[data["continents"][0]]
                if len(data["continents"]) == 1
                else "world",
                showcoastlines=False,
                showframe=False,
            ),
            height=height,
            width=width,
        )
        if path:
            file_path = path
        else:
            file_path = (
                "./docs/images/pingdom_response_country.png"
                if not self.mock
                else "./pingdom_response_country.png"
            )
        if self.docker:
            self._save_with_orca_docker(
                fig, file_path, height=height, width=width,
            )
        else:
            fig.write_image(file_path)
        if self.mock:
            fig.show()


if __name__ == "__main__":

    @click.group()
    def cli():
        """ Pingdom reporting tools command line interface. """

    def common_options(function):
        """ https://stackoverflow.com/questions/40182157 """
        options = [
            click.option(
                "--apikey",
                "-a",
                envvar="PING_TOKEN",
                help="Pingdom user's API Key.",
                required=True,
            ),
            click.option(
                "--email",
                "-e",
                envvar="PING_MAIL",
                help="Pingdom user's email.",
                required=True,
            ),
            click.option(
                "--organization",
                "-o",
                envvar="PING_ORGANIZATION",
                help="Pingdom organizations check Id number.",
                required=True,
            ),
            click.option(
                "--password",
                "-p",
                envvar="PING_PASSWORD",
                help="Pingdom user's password.",
                required=True,
            ),
            click.option(
                "--username",
                "-u",
                envvar="PING_USER",
                help="Pingdom user's name.",
                required=True,
            ),
        ]
        return functools.reduce(lambda x, opt: opt(x), options, function)

    @cli.command()
    @common_options
    @click.option("--days", "-d", default=30, help="Time range in question.")
    def average_response_time(apikey, days, email, organization, password, username):
        integration = PingdomIntegration(apikey, email, password, username)
        _average_response_time = integration.average_response_for_organization(
            organization=organization, days=days,
        )
        response_times = _average_response_time["summary"]["responsetime"][
            "avgresponse"
        ]
        status_times = _average_response_time["summary"]["status"]
        up_time = status_times["totalup"] / sum(
            [value for value in status_times.values()]
        )
        _mean = statistics.mean([i["avgresponse"] for i in response_times])
        _mean_per_country = [
            "{}: {}".format(i["countryiso"], i["avgresponse"]) for i in response_times
        ]
        _mean_per_country_string = "\n".join(_mean_per_country)
        print(
            f"Organization id: {organization}\n"
            f"Time period: last {days} day(s)\n"
            f"Up time: {'{:2.1f}%'.format(up_time * 100)}\n"
            f"Average response time (in ms): {_mean}\n"
            f"Average response time per country (in ms):\n"
            f"{_mean_per_country_string}"
        )

    @cli.command()
    @common_options
    def general_check(apikey, email, organization, password, username):
        integration = PingdomIntegration(apikey, email, password, username)
        response = integration.general_check_for_organization(organization=organization)
        _general_check = response["check"]
        print(
            f"Organization: {_general_check['name']}\n"
            f"Check resolution: {_general_check['resolution']} minute(s)\n"
            f"Last checked: {datetime.datetime.fromtimestamp(int(_general_check['lasttesttime']))}"
        )

    @cli.command()
    @common_options
    def performance_check(apikey, email, organization, password, username):
        integration = PingdomIntegration(apikey, email, password, username)
        padding = " "
        width = 10
        _performance_check = integration.performance_for_organization(
            organization=organization, hours=24
        )
        print(
            f"Organization's performance in the last 24 hours.\n"
            f"{''.join([i.ljust(width, padding) for i in ('Hour', 'Up Time', 'Down Time')])}"
        )
        for index, hour in enumerate(_performance_check["summary"]["hours"][1:]):
            print(
                "{}{}{}".format(
                    str(index + 1).ljust(width, padding),
                    str(hour["uptime"]).ljust(width, padding),
                    str(hour["downtime"]).ljust(width, padding),
                )
            )

    cli()
