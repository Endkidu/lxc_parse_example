# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 23:33:39 2022

@author: L


To do (optional):

    pydantic
    click
    comment
    unit test

"""

import json
import pandas as pd


class NetworkContainer():

    def __init__(self, name, status, created_at, memory_usage, cpu_usage, network):
        self.name = name
        self.status = status
        self.created_at = created_at
        self.memory_usage = memory_usage
        self.cpu_usage = cpu_usage
        self.network = network

    def __str__(self):
        return f'Name: {self.name}, Status: {self.status}, Created at: {self.created_at}, Memory usage: {self.memory_usage}, CPU usage: {self.cpu_usage}, Network: {self.network}'


def main():

    with open('sample-data.json') as f:
        data = json.load(f)
        df = pd.DataFrame(data)
        df1 = df[['name', 'status', 'created_at']]
        df2 = df['state'].apply(pd.Series)
        df3 = df2['memory'].apply(pd.Series)
        df3 = df3[['usage']] # memory usage
        df3.columns = ['memory_usage']
        df4 = df2['cpu'].apply(pd.Series)
        df4 = df4[['usage']] # cpu usage
        df4 = df4.rename(columns={'usage': 'cpu_usage'})
        df5 = df2['network'].apply(pd.Series)


        list_of_networks = []

        for i in range(0, len(df5)):
            if df5['eth0'][i] != '':
                try:
                    list_of_networks.append(df5['eth0'].apply(pd.Series)['addresses'].apply(pd.Series)[i].apply(pd.Series)['address'].tolist())

                except:
                    pass

        df6 = pd.DataFrame(list_of_networks).T
        df6["ip_addressess"] = df6.apply(lambda x: x[x.notna()].tolist(), axis=1)        # df7 = df6["ip_addressess"].apply(pd.Series)
        df8 = pd.concat([df1, df3, df4, df6["ip_addressess"]], axis=1)
        df8.columns = ['name', 'status', 'created_at', 'memory_usage', 'cpu_usage', 'network']
        df8['created_at'] = pd.to_datetime(df8['created_at'], utc=True)
        return df8


X = main()


if __name__ == '__main__':
    main()