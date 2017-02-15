import os
import pandas as pd
from os import listdir
from os.path import isfile, join
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import csv
import numpy as np

def csvToDataFrame(path_to_file):
    csvData = []
    data = open(path_to_file).readlines()
    for row in data:
        row = [x.rstrip() for x in row.split('\t')]
        if row != ['']:
            csvData.append(row)
    return pd.DataFrame(csvData)

def getDirNames(path_to_directory):
    names = os.listdir(path_to_directory)
    names.pop(0)
    return names

def getFileNames(path_to_directory):
    names = [f for f in listdir(path_to_directory) if isfile(join(path_to_directory, f)) and 'DS_Store' not in f and 'Sohrob' not in f]
    return names

#inputs are strings
def isSameDay(timestamp1, timestamp2):
    return datetime.fromtimestamp(float(timestamp1)).strftime('%Y-%m-%d') == datetime.fromtimestamp(float(timestamp2)).strftime('%Y-%m-%d')

def labelEachDay(subjectID):
    sleepFile = '../CS120/' + subjectID + '/ems.csv'
    sleepReport = csvToDataFrame(sleepFile)
    sleepReport = sleepReport.drop(sleepReport.columns[1:6], axis=1)
    sleepReport.columns = ['timestamp','label']
    return sleepReport

def addWifiMean(subjectID,df):
    wifiFile = '../CS120/' + subjectID + '/wif.csv'
    wifiReport = csvToDataFrame(wifiFile)

    days = len(df)

    wifiPoints = np.full((days,1),0)
    wifiCounts = np.full((days,1),0)

    # goes through the wifi data frame
    for i in range(len(wifiReport)):
        ts = wifiReport[0][i]
        accessPoints = float(wifiReport[3][i])

        # find the same day within BigFile
        for index,row in df.iterrows():
            day_ts = row['timestamp']
            day = int(row['day']) - 1
            if isSameDay(ts,day_ts):
                wifiPoints[day][0] += accessPoints
                wifiCounts[day][0] += 1
                break

    for i in range(days):
        point = wifiPoints[i][0]
        count = wifiCounts[i][0]
        wifiPoints[i][0] = (point / count) if (count > 0) else 0

    df['wifi_mean'] = wifiPoints
    return df

def createBigCSV(path_to_directory):
    participantIDs = getDirNames(path_to_directory)
    for Id in participantIDs:
        labels = labelEachDay(Id)
        labels['day'] = np.arange(1,len(labels)+1)
        labels['id'] = Id;

        df = addWifiMean(Id,labels)

        if (os.path.exists("bigFile.csv")):
            labels.to_csv('bigFile.csv', mode='a', index=False, header=False)
        else:
            labels.to_csv('bigFile.csv', index=False, header=True)

def addFeature2csv(feature_name,nparray_values):
    csv_input = pd.read_csv('bigFile.csv')
    csv_input[feature_name] = nparray_values
    csv_input.to_csv('bigFile.csv', index=False, header=True)

# counting first column as 0
def dropFeature(feature_index):
    csv_input = pd.read_csv('bigFile.csv')
    csv_input = csv_input.drop(csv_input.columns[feature_index:feature_index + 1], axis=1)
    csv_input.to_csv('bigFile.csv', index=False, header=True)
