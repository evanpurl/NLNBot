import datetime
import time

from pytz import timezone


def timetounix(inputtime):
    mst = timezone('MST')

    time_to_run = datetime.datetime.now(mst) + datetime.timedelta(hours=inputtime)

    return f'<t:{int(time.mktime(time_to_run.timetuple()))}:R>'

