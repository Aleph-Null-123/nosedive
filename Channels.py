from Timezone import Timezone
from Data import Data
from Functions import Functions
from Index import Index
from Chat import Chat
from imports import *

class Channels:
    def __init__(self, tz: Timezone = Timezone(), channels: list = None, data: Data = Data()):
        self.f = Functions()
        if channels is None:
            channels = Index(data).IDs
        self.objects = [Chat(channel, data = data) for channel in channels]
        self.tz = tz
    def DF_3D(self, real: bool = False) -> dict: #mins arg only matters if real
        new_df = {}
        if real:        
            freq = pd.tseries.offsets.DateOffset(minutes = 1)            
            earliest, latest = self.date_range()
            date_range = pd.date_range(earliest, latest, freq = freq)

            for chat in self.objects:
                data = chat.messages(self.tz)
                for i in date_range:
                    if i not in data.Timestamp:
                        data.iloc[-1] = [i, np.nan, np.nan, i.date(), i.time()]
                        data.index += 1                
                new_df[chat.channel_name] = data.sort_values('Timestamp')
        else:
            for chat in self.objects:
                new_df[chat.channel_name] = chat.messages(tz = self.tz).sort_values('Timestamp')
        return new_df

    def date_range(self) -> tuple:
        earliest, latest = None, None        
        found = False
        #beautiful
        for chat in self.objects:
            ts = list(chat.messages(self.tz).Timestamp)
            if len(ts) == 0:
                continue
            if not found:
                earliest, latest = ts[-1], ts[0]
                found = True
                continue
            if ts[-1] < earliest:
                earliest = ts[-1]
            if ts[0] > latest:
                latest = ts[0]
        return earliest, latest
    
#print(Channels().date_range())