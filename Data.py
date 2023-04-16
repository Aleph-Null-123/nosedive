from Functions import Functions
from imports import *

class Data:
    def __init__(self, path: str = ''):
        self.f = Functions()
        self.path = path
    def get(self, *paths: str) -> str:
        new_path = self.path
        for path in paths:
            new_path = os.path.join(new_path, path)
        return new_path