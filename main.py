# Given the attached CSV data file, write a function find_open_restaurants(csv_filename, search_datetime) which takes as parameters a filename and a Python datetime object and returns a list of restaurant names which are open on that date and time.  Optimized solutions are nice, but correct solutions are more important!

# Assumptions:
# * If a day of the week is not listed, the restaurant is closed on that day
# * All times are local -- don't worry about timezone-awareness
# * The CSV file will be well-formed
import csv
import re
import datetime

from dateutil import parser


# weekday indices corresponding to python's datetime module's weekdays. monday = 0
WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


def lookup(day):
    return WEEKDAYS.index(day)


class Restaurant(object):
    def __init__(self, name, hours):
        self.daily_hours = [None] * 7
        self.parse_hours(hours)

    def record_hours(self, day, opening_time, closing_time):
        index = lookup(day)
        self.daily_hours[index] = (opening_time, closing_time)

    def parse_hours(self, hours):
        # given an hours string, such as "Mon-Thu 11 am - 11 pm  / Fri-Sat 11 am - 12:30 am  / Sun 10 am - 11 pm"
        # convert that into a list of daily hours
        # for each day of the week, the opening hours are filled in. for example:
        # A restaurant open from 5pm-9pm on Sundays and 11:30am to 9:30pm on Mondays and closed the rest of the week:

        # daily_hours = [((17,0), (21,0)), ((11,30), (21,30)), None, None, None, None, None]
        # chop up the string by "/"
        specs = hours.split("/")

        def scrub(hours_string):
            for day in WEEKDAYS:
                hours_string = hours_string.replace(day, '')
            return hours_string.replace('-', '').replace('"', '')

        # each one of those, parse with a regex to figure out the days, and parse the hours
        for spec in specs:
            # hours
            opens_dt = parser.parse(scrub(spec.split(' - ')[0]))
            closes_dt = parser.parse(scrub(spec.split(' - ')[1]))
            opens = (opens_dt.hour, opens_dt.minute)
            closes = (closes_dt.hour, closes_dt.minute)
            #days
            matches = re.search(
                r"((?P<start_day>(Sun|Mon|Tue|Wed|Thu|Fri|Sat))\-(?P<end_day>(Sun|Mon|Tue|Wed|Thu|Fri|Sat))(\,\s(?P<extra_day>(Sun|Mon|Tue|Wed|Thu|Fri|Sat)))?|(?P<only_day>(Sun|Mon|Tue|Wed|Thu|Fri|Sat)))",
                spec)
            days = matches.groupdict()
            if days['start_day']:
                # there's a range, like "Mon-Thu"
                # these times apply to all days between the start and end day
                for i in range(lookup(days['start_day']), lookup(days['end_day']) + 1):
                    self.daily_hours[i] = (opens, closes)
                if days['extra_day']:
                    # there's another day appended to the range, like "Mon-Thu, Sun"
                    self.daily_hours[lookup(days['extra_day'])] = (opens, closes)

            elif days['only_day']:
                # there's just a single day in this spec, like "Sun"
                self.daily_hours[lookup(days['only_day'])] = (opens, closes)
                # self.record_hours(days['only_day'], opens, closes)

    def is_open(self, dt):
        # return true if the given datetime falls in this restaurant's hours, otherwise false
        day = dt.weekday()
        if self.daily_hours[day]:

            opens, closes = self.daily_hours[day]

            # construct a couple of datetime objects based off of the given one, to aid us in the comparison.
            opens_dt = datetime.datetime(dt.year, dt.month, dt.day, opens[0], opens[1], dt.second, dt.microsecond)
            closes_dt = datetime.datetime(dt.year, dt.month, dt.day, closes[0], closes[1], dt.second, dt.microsecond)

            if opens_dt < dt < closes_dt:
                # the given hours are within the open hours.
                return True
            else:
                return False
        else:
            # there aren't any open hours on this day.
            return False


def find_open_restaurants(csv_filename, search_datetime):
    # for each restaurant, if it's open at the given time, add to the list to be returned
    open_list = []
    with open(csv_filename) as f:
        lines = f.readlines()

    with open(csv_filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            name, hours = row
            restaurant = Restaurant(name, hours)
            if restaurant.is_open(search_datetime):
                open_list.append(name)
    return open_list

# write tests
print find_open_restaurants("rest_hours.csv", datetime.datetime(2014, 7, 15, 12, 20, 0, 0))