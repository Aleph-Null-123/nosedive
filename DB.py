import pandas as pd
pd.options.mode.chained_assignment = None
import smtplib, ssl
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import time
import pytz
import json
import os
from tzlocal import get_localzone_name
import emoji
import re
import string
import shutil
import signal, time
import openai
import warnings
import paramiko
from scp import SCPClient
import os
import uuid
import math
import traceback
import random
from cryptography.fernet import Fernet as f
import io

server = 'vergil.u.washington.edu'
username = 'arjunsn'
directory = '~/cherryblossom'
place_in = './.cherryblossom'

class SAR:
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(server, username=username, pkey=pkey)
        self.scp = SCPClient(self.ssh.get_transport())
        self.directory = directory
        self.place_in = place_in
        self.scp.get(directory, place_in, True)

    def get_text(self, file_location):
        text = None
        with open(os.path.join(self.place_in, file_location), 'r') as f:
            text = f.read().strip()
        return text

    def get_df(self, file, columns):
        return pd.read_csv(os.path.join(self.place_in, file)).\
    drop(columns = [i for i in df.columns if i not in ['ID', 'email', 'name']])

    def save_df(self, df, file):
        df.to_csv(os.path.join(self.place_in, file))

    def save(self):
        self.scp.put(self.directory, self.place_in, True)

    def close(self):
        shutil.rmtree(self.place_in)
        self.scp.close()
        self.ssh.close()

    def open(self):
        try:
            self.close()
        except:
            pass
        self.__init__()

class DB(SAR):
    def __init__(self):
        super().__init__()

    def get_openai_key(self):
        return super().get_text('openai_key')
    
    def get_app_pwd(self):
        return super().get_text('app_pwd')

    def add_contact(self, ID, email, name):
        df = super().get_df('contacts.csv', ['ID', 'email', 'name'])
        IDs = df['ID'].to_list()
        emails = df['email'].to_list()
        names = df['name'].to_list()
        IDs.append(ID)
        emails.append(email)
        names.append(name)
        df.drop(df.columns, axis = 1, inplace = True)
        df['ID'] = IDs
        df['email'] = emails
        df['name'] = names
        super().save_df(df, 'contacts.csv')
        
    def remove_contact(self, email):
        df = super().get_df('contacts.csv', ['ID', 'email', 'name'])
        df = df[df['email'] != email]
        super().save_df(df, 'contacts.csv')

    def add_info(self, ID, attributes):
        a = [f'c{i}{j}' for j in range(8) for i in range(5)]
        df = super().get_df('attributes.csv', ['ID'] + a)
        IDs = df['ID'].to_list()
        IDs.append(ID)
        att = []
        for i, j in enumerate(a):
            att.append(df[j].to_list().append(attributes[i]))

        df.drop(df.columns, axis = 1, inplace = True)
        df['ID'] = IDs
        for i, j in enumerate(a):
            df[j] = att[i]
        super().save_df(df, 'attributes.csv')

    def get_participating(self, ID):
        df = super().get_df('contacts.csv', ['ID', 'email', 'name'])
        return df[df['ID'] != ID]['ID']

    def get_info(self, ID):
        df = super().get_df('contacts.csv', ['ID', 'email', 'name'])
        return df[df['ID'] == ID]

    def get_attributes(self, ID):
        a = [f'c{i}{j}' for j in range(8) for i in range(5)]
        df = super().get_df('attributes.csv', ['ID'] + a)
        l = df[df['ID'] == ID].iloc[0].to_list()
        l.pop(0)
        return l

    def add_connection(self, ID, otherID):
        df = super().get_df('connections.csv', ['ID', 'otherID'])
        IDs = df['ID'].to_list()
        otherIDs = df['otherID'].to_list()
        IDs.append(ID)
        otherIDs.append(otherID)
        df.drop(df.columns, axis = 1, inplace = True)
        df['ID'] = IDs
        df['otherID'] = otherIDs
        super().save_df(df, 'connections.csv')
        
#print(DB().get_openai_key())
