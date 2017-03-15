import os
import pandas as pd

from os import listdir
from os.path import isfile, join
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

def csvToDataFrame(path_to_file):
    csvData = []
    data = open(path_to_file).readlines()
    for row in data:
        row = [x.rstrip() for x in row.split('\t')]
        csvData.append(row)
    return pd.DataFrame(csvData)

def getDirNames(path_to_directory):
    names = os.listdir(path_to_directory)
    names.pop(0)
    return names

def getFileNames(path_to_directory):
    names = [f for f in listdir(path_to_directory) if isfile(join(path_to_directory, f)) and 'DS_Store' not in f and 'Sohrob' not in f]
    print (names)

#inputs are strings
def isSameDay(timestamp1, timestamp2):
    if '"' in timestamp1:
        timestamp1 = timestamp1.replace('"','')
    if '"' in timestamp2:
        timestamp2 = timestamp2.replace('"', '')
    date1 = datetime.utcfromtimestamp(float(timestamp1)).strftime('%Y-%m-%d')
    date2 = datetime.utcfromtimestamp(float(timestamp2)).strftime('%Y-%m-%d')
    return date1 == date2

def visualizeTouchCount(subjectID):
    touchFile = '../CS120/' + subjectID + '/tch.csv'
    sleepFile = '../CS120/' + subjectID + '/ems.csv'
    touchReport = csvToDataFrame(touchFile)
    sleepReport = csvToDataFrame(sleepFile)
    normal_ts = []
    normal_num = []
    partial_ts = []
    partial_num = []
    off_ts = []
    off_num = []

    day = 0
    for i in range(len(touchReport)):
        ts = touchReport[0][i]
        touchCounts = touchReport[2][i]

        while not isSameDay(ts, sleepReport[0][day]):
            day += 1

        if sleepReport[6][day] == 'normal':
            normal_ts.append(ts)
            normal_num.append(touchCounts)
        elif sleepReport[6][day] == 'partial':
            partial_ts.append(ts)
            partial_num.append(touchCounts)
        elif sleepReport[6][day] == 'off':
            off_ts.append(ts)
            off_num.append(touchCounts)

    plt.plot(normal_ts, normal_num, 'r.', partial_ts, partial_num, 'b.', off_ts, off_num, 'g.')
    plt.ylabel("Touch Count")
    plt.xlabel('Timestamp')

    blue_line = mlines.Line2D([], [], color='blue', marker='.',
                              markersize=15, label='Partial Workday')
    red_line = mlines.Line2D([], [], color='red', marker='.',
                              markersize=15, label='Workday')
    green_line = mlines.Line2D([], [], color='green', marker='.',
                              markersize=15, label='Off')
    plt.legend(handles=[blue_line,red_line,green_line])

    plotName = "Touch Visualization for " + subjectID
    plt.title(plotName)

    plotFileName = "../Visualization/touchCount_V_"+subjectID + ".png"
    plt.savefig(plotFileName,dpi=1000)

def visualizeTouchDelay(subjectID):
    touchFile = '../CS120/' + subjectID + '/tch.csv'
    sleepFile = '../CS120/' + subjectID + '/ems.csv'
    touchReport = csvToDataFrame(touchFile)
    sleepReport = csvToDataFrame(sleepFile)
    normal_ts = []
    normal_num = []
    partial_ts = []
    partial_num = []
    off_ts = []
    off_num = []

    day = 0
    for i in range(len(touchReport)):
        ts = touchReport[0][i]
        lastTouchDelay = touchReport[1][i]

        while not isSameDay(ts, sleepReport[0][day]):
            day += 1

        if sleepReport[6][day] == 'normal':
            normal_ts.append(ts)
            normal_num.append(lastTouchDelay)
        elif sleepReport[6][day] == 'partial':
            partial_ts.append(ts)
            partial_num.append(lastTouchDelay)
        elif sleepReport[6][day] == 'off':
            off_ts.append(ts)
            off_num.append(lastTouchDelay)

    plt.plot(normal_ts, normal_num, 'r.', partial_ts, partial_num, 'b.', off_ts, off_num, 'g.')
    plt.ylabel('Last touch delay')
    plt.xlabel('Timestamp')

    blue_line = mlines.Line2D([], [], color='blue', marker='.',
                              markersize=15, label='Partial Workday')
    red_line = mlines.Line2D([], [], color='red', marker='.',
                              markersize=15, label='Workday')
    green_line = mlines.Line2D([], [], color='green', marker='.',
                              markersize=15, label='Off')
    plt.legend(handles=[blue_line,red_line,green_line])

    plotName = "Last Touch Delay Visualization for " + subjectID
    plt.title(plotName)
    plotFileName = "../Visualization/touchdelay_V_"+subjectID + ".png"
    plt.savefig(plotFileName,dpi=1000)

def visualizeWifi(subjectID):
    wifiFile = '../CS120/' + subjectID + '/wif.csv'
    sleepFile = '../CS120/' + subjectID + '/ems.csv'
    wifiReport = csvToDataFrame(wifiFile)
    sleepReport = csvToDataFrame(sleepFile)
    normal_ts = []
    normal_num = []
    partial_ts = []
    partial_num = []
    off_ts = []
    off_num = []

    day = 0
    for i in range(len(wifiReport)):
        ts = wifiReport[0][i]
        accessPoints = wifiReport[3][i]

        while not isSameDay(ts, sleepReport[0][day]):
            day += 1

        if sleepReport[6][day] == 'normal':
            normal_ts.append(ts)
            normal_num.append(accessPoints)
        elif sleepReport[6][day] == 'partial':
            partial_ts.append(ts)
            partial_num.append(accessPoints)
        elif sleepReport[6][day] == 'off':
            off_ts.append(ts)
            off_num.append(accessPoints)

    plt.plot(normal_ts, normal_num, 'r.', partial_ts, partial_num, 'b.', off_ts, off_num, 'g.')
    plt.ylabel('Number of Wifi Access Points')
    plt.xlabel('Timestamp')

    blue_line = mlines.Line2D([], [], color='blue', marker='.',
                              markersize=15, label='Partial Workday')
    red_line = mlines.Line2D([], [], color='red', marker='.',
                              markersize=15, label='Workday')
    green_line = mlines.Line2D([], [], color='green', marker='.',
                              markersize=15, label='Off')
    plt.legend(handles=[blue_line,red_line,green_line])

    plotName = "Wifi Visualization for " + subjectID
    plt.title(plotName)
    plotFileName = "../Visualization/wifi_V_"+subjectID + ".png"
   # plt.show()
    plt.savefig(plotFileName,dpi=1000)

def csvToArr(path_to_file):
    sensor = []
    label = []
    data = open(path_to_file).readlines()
    for row in data:
        row = [x.rstrip() for x in row.split('\t')]
        row = row[0].split(',')
        sensor.append(row[0])
        label.append(row[1])
    return pd.DataFrame(csvData)

############ RUN EXAMPLE ####################
participantID = '25349'
visualizeTouchCount(participantID)
visualizeTouchDelay(participantID)
visualizeWifi(participantID)