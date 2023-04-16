from Chat import Chat
from Functions import Functions
from imports import *

class Plots:
    def __init__(self, *chats: Chat):
        self.f = Functions()
        self.frames = [i.count() for i in chats]
    def plot(self):
        plt.figure()
        for i in self.frames:
            plt.plot(i.index, i[0])
        plt.title('Comparison')
        plt.xticks(rotation=45, ha="right")
        plt.show()
        
#Plots()