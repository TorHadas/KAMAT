#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime


def heb_to_date(heb):

    split = heb.split()
    day = int(split[0])
    month = split[1].split(',')[0].encode('utf-8', 'ignore')
    hour_minute = split[2]
    hour = int(hour_minute.split(':')[0])
    minute = int(hour_minute.split(':')[1])

    # TODO: fix month names
    if month == 'ינואר' or month == 'ינו׳' or month == 'Jan':
        month = 1
    elif month == 'פברואר' or month == 'פבר׳' or month == 'Feb':
        month = 2
    elif month == 'מרץ' or month == 'מרס' or month == 'Mar':
        month = 3
    elif month == 'אפריל' or month == 'אפר׳' or month == 'Apr':
        month = 4
    elif month == 'מאי' or month == 'May':
        month = 5
    elif month == 'יוני' or month == 'June':
        month = 6
    elif month == 'יולי' or month == 'July':
        month = 7
    elif month == 'אוגוסט' or month == 'אוג׳' or month == 'Aug':
        month = 8
    elif month == 'ספטמבר' or month == 'ספט׳' or month == 'Sep':
        month = 9
    elif month == 'אוק׳' or month == 'אוקטובר' or month == 'Oct':
        month = 10
    elif month == 'נובמבר' or month == 'נוב׳' or month == 'Nov':
        month = 11
    elif month == 'דצמבר' or month == 'דצמ׳' or month == 'Dec':
        month = 12
    else:
        print('ERROR parsing date')
        raise NameError(month)  # TODO : is it working?

    this_year = datetime.now().year
    this_month = datetime.now().month

    # TODO : better yuristic?
    if month < this_month:
        year = this_year + 1
    else:
        year = this_year

    datetime_object = datetime(year, month, day, hour, minute)

    return datetime_object
