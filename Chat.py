from Data import Data
from Timezone import Timezone
from Functions import Functions
from Index import Index
from imports import *

class Chat:
    def __init__(self, channel_name: str, DM: bool = False, data: Data = Data(), tz: Timezone = Timezone()):
        self.f = Functions()
        if DM:
            self.channel_name = self.f.dm(channel_name)
        else:
            self.channel_name = channel_name
        self.DM = channel_name.startswith('Direct Message with ')
        self.ID = Index(data).search(self.channel_name)
        self.path = self.f.msg_path(self.ID)
        self.data = pd.read_csv(data.get(self.path))
        self.tz = tz

    def messages(self, tz: Timezone = None) -> pd.DataFrame:
        if tz is None:
            tz = self.tz
        data = self.data.copy()
        data['Timestamp'] = [tz.offset_time(self.f.to_time(s)) for s in data.Timestamp]
        data['dates'] = [s.date() for s in data.Timestamp]
        data['times'] = [s.time() for s in data.Timestamp]
        data['Channel'] = [self.channel_name for s in data.Timestamp]
        return data

    def count(self, gaps: bool = True, dr: tuple = None, data: pd.DataFrame = None, tz: Timezone = Timezone()) -> pd.DataFrame:
        if data is None:
            data = self.messages(tz)        
        data = data.value_counts('dates').to_frame().sort_values('dates')
        if dr is None:
            a, b = data.index[0], data.index[-1]
        else:
            a, b = dr
        if gaps:
            missing = [i.date() for i in pd.date_range(a, b) 
               if i.date() not in data.index]
            data = pd.DataFrame(list(data[0]) + [0] * len(missing),
                               list(data.index) + missing).sort_index()
        return data

    def total_msgs(self) -> int:
        return len(self.data)

    def plot(self):
        plt.figure()
        plt.plot(self.count().index, self.count()[0])
        plt.title(f'{self.channel_name}')
        plt.xticks(rotation=45, ha="right")
        plt.show()

    def __str__(self):
        return f'Channel: {self.channel_name}\nID: {self.ID}'

#print(Chat("sam!#6054", DM = True).total_msgs())