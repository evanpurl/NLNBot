from datetime import datetime, timedelta
from time import mktime
from pytz import timezone


async def timetounix(inputtime):
    mst = timezone('MST')

    time_to_run = datetime.now(mst) + timedelta(hours=inputtime)

    return f'<t:{int(mktime(time_to_run.timetuple()))}:R>'
