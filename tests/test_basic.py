from datetime import date

from BillMind import main


def test_week_range():
    start, end = main.get_current_week_range(date(2026, 3, 2))
    assert start.weekday() == 0  # Monday
    assert end.weekday() == 6    # Sunday
