#!/bin/env python3
# -*- coding: utf-8 -*-

"""
Ops teams often drop all tasks at hand when there are incidents or requets for help.
This might not be the most efficient way to handle this.
supporter_of_the_week creates a schedule with a team member on call to do first response.
"""

import argparse
import datetime
from itertools import cycle
from random import randint, shuffle

from collections import namedtuple
from icalendar import Calendar, Event
from workalendar.europe import Netherlands


class SupportCalendar():
    """
    Represents a support calendar.
    """

    def __init__(
        self, supporters: list, shuffle_supporters: bool = False, start_date: str = None
    ):
        """main.
        Make a schedule and load it onto the class.


        :param supporters:
        :type supporters: list
        :param shuffle_supporters:
        :type shuffle_supporters: bool
        :param start_week:
        :type start_week: int
        """

        self.cal = Netherlands()

        self.table = []

        today = datetime.date.today().isocalendar()

        if start_date is None:
            start = datetime.date.fromisocalendar(
                year=today.year, week=today.week, day=1
            )
        else:
            start = datetime.datetime.strptime(start_date, "%d-%m-%Y").date()

        end = datetime.date.fromisocalendar(year=today.year + 1, week=today.week, day=5)

        if shuffle_supporters:
            shuffle(supporters)

        wheel = cycle(supporters)
        ical = Calendar()
        day = start

        event_id = randint(int(1e9), int(10e10))

        ScheduleRow = namedtuple(
            "ScheduleRow", ["weeknr", "supporter", "first_workday", "last_workday"]
        )

        while day < end:
            first_workday = self.skip_holiday(day)
            # last_workday is friday or the first non holiday looking backwards.
            last_workday = self.skip_holiday(
                day + datetime.timedelta(days=5), backwards=True
            )
            supporter = next(wheel)

            self.table.append(
                ScheduleRow(
                    day.isocalendar().week,
                    supporter,
                    first_workday.strftime("%d/%m %Y"),
                    last_workday.strftime("%d/%m"),
                )
            )
            day += datetime.timedelta(days=7)
            event = Event()
            event.add("dtstart", first_workday)
            # Microsoft outlook shows the event as if it ends one day before
            # the end date.
            event.add("dtend", last_workday + datetime.timedelta(days=1))
            event.add("summary", f"{supporter} is supporter of the week")
            event.add("description", f"{supporter} is supporter of the week")

            event["uid"] = event_id
            event_id += 1

            ical.add_component(event)

            self.ical = ical.to_ical()

    def skip_holiday(self, day: datetime.date, backwards=False) -> datetime.date:
        """
        Advance day until day without public holiday is found

        :param day:
        :type day: datetime.date
        :param backwards:
        :rtype: datetime.date
        """
        if self.cal.is_working_day(day):
            return day
        # if reversed, delta is backwards.
        return self.skip_holiday(
            day + datetime.timedelta(days=-1 if backwards else 1), backwards=backwards
        )


    @property
    def markdown(self) -> str:
        """
        Create markdown representation of schedule.
        """
        table = ["| weeknr | supporter | first day | last day |"]
        table.append("|------|------|------|------|")
        for row in self.table:
            table.append(
                f"| {row.weeknr:<3} | {row.supporter} | {row.first_workday} | {row.last_workday} |"
            )
        return "\n".join(table)

    @property
    def html(self) -> str:
        """
        Create html representation of schedule.
        Maybe use templating engine?
        """
        table = [
            """<table>
                  <tr>
                    <th>weeknr</th>
                    <th>supporter</th>
                    <th>first day</th>
                    <th>last day</th>
                  </tr>
                 """
        ]
        for row in self.table:
            table.append(
                f"""
                <tr>
                    <th>{row.weeknr:<3}</th>
                    <th>{row.supporter}</th>
                    <th>{row.first_workday}</th>
                    <th>{row.last_workday}</th>
                </tr>
                """
            )

        table.append("</table>")
        return "\n".join(table)


def main():
    """
    Parse arguments, print markdown table.
    Write MS Outlook compatible ical file.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--start-date",
        type=str,
        dest="start_date",
        help="date for first week in calendar'%d-%m-%Y'",
        required=False,
    )

    parser.add_argument(
        "--supporters",
        dest="supporters",
        type=str,
        help="Comma separated list of supporters.",
        required=True,
    )

    parser.add_argument(
        "--shuffle",
        action="store_true",
        dest="shuffle_supporters",
        help="Shuffle the order of the supporters.",
        required=False,
    )

    args = parser.parse_args()
    args.supporters = args.supporters.split(",")

    calendar = SupportCalendar(**vars(args))
    print(calendar.markdown)
    with open("supporters.ical", "wb") as f:
        f.write(calendar.ical)


if __name__ == "__main__":
    main()
