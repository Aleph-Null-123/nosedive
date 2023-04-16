from Functions import Functions
from imports import *

class Timezone:
    def __init__(self, name: str = '', offset: dt.timedelta = dt.timedelta(0)):
        self.f = Functions()
        if name == 'LOCAL':
            name = self.local_name()
            offset = self.local_offset()
        self.offset = offset
        self.name = name

    def offset_time(self, utc_time: dt.datetime = dt.datetime.now(pytz.timezone('UTC'))) -> dt.datetime:
        return utc_time + self.offset

    def local_offset(self, utc_time: dt.datetime = dt.datetime.now()) -> dt.timedelta:
        timezone = pytz.timezone(self.local_name())
        offset = timezone.localize(utc_time).strftime('%z')
        offset = int(offset)
        hrs, mins = offset//100, offset % 100
        return dt.timedelta(hours = hrs, minutes = mins)

    def local_name(self) -> str:
        return get_localzone_name()
    
#print(Timezone().local_name())