import pytest

import supporter_of_the_week


def test_table():
    cal = supporter_of_the_week.SupportCalendar(
        start_date="23-12-2024",
        supporters=["kwik", "kwek", "kwak"],
        end_date="15-01-2026",
    )
    assert cal.table[-1][2] == "12/01 2026"


def test_ical():
    cal = supporter_of_the_week.SupportCalendar(
        start_date="01-01-2025",
        end_date="01-01-2026",
        supporters=["kwik", "kwek", "kwak", "donald"],
    )
    last_event = str(cal.ical).split("\\r\\n")[-9:]
    # pop the random uuid
    last_event.pop(4)

    assert last_event == [
        "BEGIN:VEVENT",
        "SUMMARY:kwik is supporter of the week",
        "DTSTART;VALUE=DATE:20251231",
        "DTEND;VALUE=DATE:20260106",
        "DESCRIPTION:kwik is supporter of the week",
        "END:VEVENT",
        "END:VCALENDAR",
        "'",
    ]
