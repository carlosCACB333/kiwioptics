from django.db.models import Func
from django.db import models

def monthdelta(date, delta):
    m = (date.month+delta) % 12
    if delta > date.month:
        y = date.year-1
    else:
        y = date.year
    if not m:
        m = 12
    d = min(date.day, [31,
                       29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m-1])
    return date.replace(day=d, month=m, year=y)


class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()


class Year(Func):
    function = 'EXTRACT'
    template = '%(function)s(YEAR from %(expressions)s)'
    output_field = models.IntegerField()


class Day(Func):
    function = 'EXTRACT'
    template = '%(function)s(DAY from %(expressions)s)'
    output_field = models.IntegerField()


class Week(Func):
    function = 'EXTRACT'
    template = '%(function)s(WEEK from %(expressions)s)'
    output_field = models.IntegerField()


class Hour(Func):
    function = 'EXTRACT'
    template = '%(function)s(HOUR from %(expressions)s)'
    output_field = models.IntegerField()
