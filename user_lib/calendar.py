import user_lib.file_mgmt as fileMgmt
import user_lib.scrapey as scrapey
import user_lib.general as tools
import global_variables as var
from datetime import datetime, timezone


# accepts datetime utcnow
def is_business_hours(date):
    try:
        time = date.strftime('%H:%M:%S')
        if var.market_open <= time < var.market_close:
            return is_trading_day(blank_time_on_date(date))
        else:
            return False
    except Exception as e:
        print(e)


# accepts datetime date
def is_trading_day(date):
    try:
        if is_weekday(date):
            # check if holiday, scrape from https://www.nyse.com/markets/hours-calendars if there is no save file or database entry for 2022
            # will not worry about historical holidays only current so I don't try to get data those days
            # may care about previous holidays later, they will be manually entered, the furthest back one could be a global limit on how far back I will query
            # I am not going to compute each holiday as they have changed and will still change, better to get from the source,
            # if i do compute my own I will have to monitor and update
            # could give alerts about upcoming holidays
            # maybe give a new year alert to tell you to check for an update to calendars
            # an idea is alerts day of/day before
            # below a tray listing upcoming alerts for the next week or two
            if date not in var.holidays_list:
                return True
        return False
    except Exception as e:
        print(e)


# accepts datetime
def is_weekday(date):
    try:
        if date.weekday() > 4:
            return False
        else:
            return True
    except Exception as e:
        print(e)


def check_holiday_cache(path, ext, current_year, next_year):
    try:
        fileMgmt.create_file(path, current_year, ext)
        if fileMgmt.file_empty(path, current_year, ext):
            cache_holidays(path, current_year, ext)
        fileMgmt.create_file(path, next_year, ext)
        if fileMgmt.file_empty(path, next_year, ext):
            cache_holidays(path, next_year, ext)
    except Exception as e:
        print(e)


def cache_holidays(path, year, ext):
    try:
        results = parse_holiday_table(year)
        fileMgmt.dump_dictionary_in_file(path, year, ext, results)
    except Exception as e:
        print(e)


def parse_holiday_table(year):
    try:
        holiday_table = scrapey.scrape(var.nyse_hours_url, 'table', 'table', None)
        header = holiday_table.find_all('th')
        header = [span.get_text() for span in header]
        holiday_col = header.index('Holiday')
        year_col = header.index(year)
        rows = holiday_table.find_all('tr')
        results = {}
        for row in rows:
            if not row.find_all('th'):  # not the header row
                cells = scrapey.gimmie_contents_as_text(row, 'td')
                results[cells[holiday_col]] = cells[year_col]
        return results
    except Exception as e:
        print(e)


# TODO: for now half day holidays will be treated as full holidays... Will be vetted from table in interface where user selects holiday 1/2 days
def read_holidays(path, ext, current_year, next_year):
    def format_holidays(holidays, year):
        try:
            for h in holidays:
                val = holidays[h]
                if tools.is_date(val):
                    val = tools.parse_date(val + ' ' + year)
                    holidays[h] = val.replace(tzinfo=timezone.utc)
                else:
                    holidays[h] = ''
            return holidays
        except Exception as e:
            print(e)
    current_year_holidays = fileMgmt.read_dictionary_file(path, current_year, ext)
    current_year_holidays = format_holidays(current_year_holidays, current_year)
    next_year_holidays = fileMgmt.read_dictionary_file(path, next_year, ext)
    next_year_holidays = format_holidays(next_year_holidays, next_year)
    return {'current_year': current_year_holidays, 'next_year': next_year_holidays}


def blank_time_on_date(date):
    try:
        return date.replace(hour=0, minute=0, second=0, microsecond=0)
    except Exception as e:
        print(e)
