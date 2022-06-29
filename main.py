import global_variables as var
from datetime import datetime, timezone
import user_lib.calendar as cal
import time
import schedule
import multiprocessing
import smtplib
import tests.calendar_test as testin
import unittest
import importlib


# 0.1
# with the holiday to file working, next do:
#       a file reader that sets the contents to a dictionary as a global variable
#       update the is_business_day to use this
#       add is_business_hours
#       a loop to update evey minute or x seconds, to check time and do stuff
#       should create a new est day timer - have working demos in place
#       hard coded utc changed to datetime utc
#       create a new email
#       update sender in send_email
#       email to text message
#       store passwords and email as env var or conf file
# clean everything, includes refactoring to PEP 8, and moving functions to libraries
# tests for everything
#       cancel ortex... not my concern now, may have some use in stock utilization, but not my concern now
#       git acct and first commit... make private
# start aws, delay this, cost is a concern, in meantime research other cloud providers
# create a notes file transcribe a lot of what gherk said and add a todo

# 0.2
# free account for https://polygon.io/, may later move to https://eodhistoricaldata.com/
# get data be sure to save as test data (5 req a day limit) but don't need to otherwise
# bs calculations, and optimizer to find imp vol, gamma max, delta neutral, etc...
# more tests
# commit

# 1.0 - first version of any value
# new data source,
# set to stream through day with notifications and basic disply of greeks, price, and console drawer
# will likely use PyQt
# more tests
# commit

# MISC?
# I will likely need threading... see synchronized?  My time_loop will likely need it's own thread
# read some tutorial in this
# likely most app will use multithreading but the optimization may use multiprocessing
# # useful https://stackoverflow.com/questions/31123293/is-python-a-good-choice-to-build-a-desktop-application
# to speed up the app look at Cython
# run daily with daily updates, this will require creating shared libraries between the aws code and home code
# for multithreading https://stackoverflow.com/questions/58375177/multiprocessing-with-schedule-in-python
# https://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python
# maybe the best demo https://www.analyticsvidhya.com/blog/2021/04/a-beginners-guide-to-multi-processing-in-python/

# EMAIL SERVER
# https://www.youtube.com/watch?v=JRCJ6RtE3xU
# to forward as text message https://www.cnet.com/tech/services-and-software/auto-forward-important-email-to-your-phone-as-a-text-message/
# https://mail.google.com/mail/u/0/#settings/fwdandpop
# add a forwarding address
# phonenumber @ msg.telus.com
# found from https://www.email-unlimited.com/stuff/send-email-to-phone.htm
# if stuck with auth https://stackoverflow.com/questions/25944883/how-to-send-an-email-through-gmail-without-enabling-insecure-access
# auth problems often resolved here https://console.cloud.google.com/apis/credentials

# TIME: it is important to note that unless displayed, ALL times MUST BE SET to UTC


class Option:
    def __init__(self, date, strike, price):
        self.experiation = date
        self.strike = strike
        self.price = price


def check_data_caches():
    path = 'cached_data/nyse_holidays/'
    ext = 'txt'
    current_year = var.current_year
    next_year = var.next_year
    cal.check_holiday_cache(path, ext, current_year, next_year)
    holidays = cal.read_holidays(path, ext, current_year, next_year)
    var.set_holidays(holidays)


def on_launch():
    check_data_caches()


def time_loop(wait_time):
    """
    wait_time is in seconds must be 60 or less.  may pass a function to do stuff
    not worrying about microseconds
    """
    try:
        print(datetime.now().second)
        if 60 % wait_time == 0 and wait_time > 0:
            wait_for = find_time_to_next_wait(wait_time)
            time.sleep(wait_for)
            # do_stuff
            print(datetime.now().second)
            time_loop(wait_time)  # This function cannot make up for lost time... as in, if the function runs longer than the wait_time... oh well
            # may put in a way to end this
    except Exception as e:
        print(e)


def find_time_to_next_wait(wait_time):
    try:
        if 60 % wait_time == 0 and wait_time > 0:
            current_seconds = datetime.now().second
            current_chunk = current_seconds / wait_time
            next_chunk = int(current_chunk) + 1
            return int(next_chunk * wait_time) - int(current_chunk * wait_time)
    except Exception as e:
        print(e)


def sleepy_man():
    print('Starting to sleep')
    time.sleep(1)
    print('Done sleeping')


def once_a_day():
    t = datetime.today().utcnow()
    print("I'm working..." + t.strftime('%H:%M'))


def send_email(email):
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()  # identify self with mail server
            smtp.starttls()  # encrypts traffic
            smtp.ehlo()
            smtp.login(var.email_server_address, var.email_server_password)
            subject = 'testing my code'
            body = 'this is a test'
            msg = f'Subject: {subject}\n\n{body}'
            smtp.sendmail(var.email_server_address, email, msg)  # sender, receiver, message
    except Exception as e:
        print(e)


# once a day should either be a thread or just throw it in the main loop
# main loop will call schedule.run_pending() whenever done the loop
# schedule.every().day.at("01:00").do(job,'It is 01:00') will be in init once
# if __name__ == '__main__':
#     print('working')
#     on_launch()
#     cal.is_business_hours(datetime.today().utcnow())
#     # multiprocessing does not seem to like two schedules running within the process
#     # multiprocessing will likely be useful for optimization of greeks
#     # multithreading will likely be more useful from an interface perspective
#     # I don't think either are really needed right now...  keep a demo commented out
#     p1 = multiprocessing.Process(target=sleepy_man)
#     p2 = multiprocessing.Process(target=sleepy_man)
#     p1.start()
#     p2.start()
#     # p1.join() # use join to wait before the main process proceeds
#     # p2.join()
#     # the example here: the long datetime is a string "13:30"
#     schedule.every().day.at(datetime.strptime('13:30', var.time_format).replace(tzinfo=timezone.utc).strftime(var.time_format)).do(once_a_day)
#     schedule.run_pending()
#     print('past pending')
#     # once_a_day()
#
#     send_email(var.user_email)
#
#     time_loop(60)


if __name__ == '__main__':
    mod = importlib.import_module('.calendar_test', package='tests')
    unittest.main(module=mod)  # this is how to call tests
