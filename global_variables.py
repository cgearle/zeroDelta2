from datetime import datetime, timezone
import os

ticker = 'GME'
nyse_hours_url = 'https://www.nyse.com/markets/hours-calendars'
current_year = str(datetime.now().year)
next_year = str(datetime.now().year + 1)
holidays_dict = None
holidays_list = None
time_format = '%H:%M'
market_open = datetime.strptime('13:30', time_format).replace(tzinfo=timezone.utc).strftime(time_format)  # 9:30am est
market_close = datetime.strptime('20:00', time_format).replace(tzinfo=timezone.utc).strftime(time_format)  # 4:00pm est
email_server_address = os.environ.get('Email_Server_Address')
email_server_password = os.environ.get('Email_Server_Password')  # gmail app password for the server email
# will remove user once db is created
user = 'cearle'
user_email = 'chris.g.earle@gmail.com'


def set_holidays(h_dict):
    try:
        global holidays_dict
        holidays_dict = h_dict
        holiday_years = list(h_dict)
        all_holidays_arr = []
        for yr in holiday_years:
            holidays_for_yr = list(h_dict.get(yr).values())
            all_holidays_arr += holidays_for_yr
        global holidays_list
        holidays_list = all_holidays_arr
    except Exception as e:
        print(e)
