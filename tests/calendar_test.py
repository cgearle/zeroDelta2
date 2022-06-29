import user_lib.calendar as cal
import unittest
from datetime import datetime, timezone
import global_variables as var
import user_lib.general as tools


class Test(unittest.TestCase):
    """
    test that when parsing the nyse holidays table from the website that at least half the read dates are dates
    """
    def test_if_has_holiday_table(self):
        try:
            result = cal.parse_holiday_table(var.current_year)
            dates = list(result.values())
            date_count = 0
            total_dates = len(dates)
            for d in dates:
                if tools.is_date(d):
                    date_count += 1
            self.assertTrue(date_count > total_dates / 2, "it looks like the nyse holiday table isn't being properly read")
        except Exception as e:
            print(e)

    # next: tests should run as a new instance, this seems more like a bridge you will cross when deploying to the cloud
    def test_business_hours(self):
        try:
            test_current_year = '2022'
            test_next_year = '2023'
            holidays = cal.read_holidays('test_data/nyse_holidays/', 'txt', test_current_year, test_next_year)
            var.set_holidays(holidays)
            test_date = datetime(2022, 6, 9, 18, 9, 9).replace(tzinfo=timezone.utc)
            self.assertTrue(cal.is_business_hours(test_date), 'is business hours')
            test_date = datetime(2022, 6, 9, 23, 9, 9).replace(tzinfo=timezone.utc)
            self.assertFalse(cal.is_business_hours(test_date), 'not business hours')
            test_date = datetime(2022, 6, 9, 4, 9, 9).replace(tzinfo=timezone.utc)
            self.assertFalse(cal.is_business_hours(test_date), 'not business hours')
            test_date = datetime(2022, 6, 11, 18, 9, 9).replace(tzinfo=timezone.utc)
            self.assertFalse(cal.is_business_hours(test_date), 'weekend is not business hours')
            test_date = datetime(2022, 6, 20, 18, 9, 9).replace(tzinfo=timezone.utc)
            self.assertFalse(cal.is_business_hours(test_date), 'holiday is not business hours')
            test_date = datetime(2023, 6, 9, 18, 9, 9).replace(tzinfo=timezone.utc)
            self.assertTrue(cal.is_business_hours(test_date), 'is business hours')
            test_date = datetime(2023, 6, 9, 23, 9, 9).replace(tzinfo=timezone.utc)
            self.assertFalse(cal.is_business_hours(test_date), 'not business hours')
            test_date = datetime(2023, 6, 9, 4, 9, 9).replace(tzinfo=timezone.utc)
            self.assertFalse(cal.is_business_hours(test_date), 'not business hours')
            test_date = datetime(2023, 6, 11, 18, 9, 9).replace(tzinfo=timezone.utc)
            self.assertFalse(cal.is_business_hours(test_date), 'weekend is not business hours')
            test_date = datetime(2023, 6, 19, 18, 9, 9).replace(tzinfo=timezone.utc)
            self.assertFalse(cal.is_business_hours(test_date), 'holiday is not business hours')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    unittest.main()
