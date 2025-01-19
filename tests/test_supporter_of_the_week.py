import pytest

import supporter_of_the_week


def test_table():
    cal = supporter_of_the_week.SupportCalendar(
        start_date="23-12-2024", supporters=["kwik", "kwek", "kwak"]
    )
    assert cal.table[-1][2] == "12/01 2026"


def test_ical():
    cal = supporter_of_the_week.SupportCalendar(
        start_date="01-01-2025", supporters=["kwik", "kwek", "kwak", "donald"]
    )
    last_event = str(cal.ical).split("\\r\\n")[-9:]
    # pop the random uuid
    last_event.pop(4)
    assert last_event == [
        "BEGIN:VEVENT",
        "SUMMARY:kwak is supporter of the week",
        "DTSTART;VALUE=DATE:20260114",
        "DTEND;VALUE=DATE:20260120",
        "DESCRIPTION:kwak is supporter of the week",
        "END:VEVENT",
        "END:VCALENDAR",
        "'",
    ]
