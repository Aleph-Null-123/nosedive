from Data import Data
from Functions import Functions
from imports import *

class Index:
    def __init__(self, data: Data = Data()):
        self.f = Functions()
        self.index = None
        with open(data.get('messages', 'index.json'), 'r') as f:
            self.index = json.load(f)                            
        self.IDs = {val: key for key, val in self.index.items()}
        self.IDs.pop(None)
    def search(self, channel_name: str, DM: bool = False) -> int:
        if DM:
            return self.IDs[self.f.dm(channel_name)]
        else:
            return self.IDs[channel_name]
        
#Index()