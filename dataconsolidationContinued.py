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
        row = [x.strip('"') for x in row]
        if row != ['']:
            csvData.append(row)
    return pd.DataFrame(csvData)

def getDirNames(path_to_directory):
    names = os.listdir(path_to_directory)
    # names.pop(0)
    return names

def getFileNames(path_to_directory):
    names = [f for f in listdir(path_to_directory) if isfile(join(path_to_directory, f)) and 'DS_Store' not in f and 'Sohrob' not in f]
    return names

def isSameDay(timestamp1, timestamp2):
    if '"' in timestamp1:
        timestamp1 = timestamp1.replace('"','')
    if '"' in timestamp2:
        timestamp2 = timestamp2.replace('"', '')
    date1 = datetime.utcfromtimestamp(float(timestamp1)).strftime('%Y-%m-%d')
    date2 = datetime.utcfromtimestamp(float(timestamp2)).strftime('%Y-%m-%d')
    return date1 == date2

def timeDifference(timestamp1, timestamp2):
    if '"' in timestamp1:
        timestamp1 = timestamp1.replace('"','')
    if '"' in timestamp2:
        timestamp2 = timestamp2.replace('"', '')
    date1 = datetime.utcfromtimestamp(float(timestamp1)).strftime('%Y-%m-%d')
    date2 = datetime.utcfromtimestamp(float(timestamp2)).strftime('%Y-%m-%d')
    return abs(date1 - date2)

def isEarlier(timestamp1, timestamp2):
    if '"' in timestamp1:
        timestamp1 = timestamp1.replace('"','')
    if '"' in timestamp2:
        timestamp2 = timestamp2.replace('"', '')
    date1 = datetime.utcfromtimestamp(float(timestamp1)).strftime('%Y-%m-%d')
    date2 = datetime.utcfromtimestamp(float(timestamp2)).strftime('%Y-%m-%d')
    return date1 < date2

def labelEachDay(subjectID):
    sleepFile = '../CS120/' + subjectID + '/ems.csv'
    sleepReport = csvToDataFrame(sleepFile)
    sleepReport = sleepReport.drop(sleepReport.columns[1:6], axis=1)
    sleepReport.columns = ['timestamp','label']
    return sleepReport

def touchEvents(subjectID,df,days):
    """calculate the total number of touch events each day"""
    touchFile = '../CS120/' + subjectID + '/tch.csv'
    touchReport = csvToDataFrame(touchFile)
    # create numpy array to keep track of the total number of touches per day
    totalTouches = np.full((days,1),0)
    lengthTouchReport = len(touchReport)

    c = 0
    # loop through the total number of days
    for i in range(days):
        if c == lengthTouchReport:
            break
        # i = 52 causes issues
        # add all of the touch events together within the same day
        while (isEarlier(touchReport.ix[c,0],df.ix[i,'timestamp'])):
            if c < lengthTouchReport-1:
                c += 1
            else:
                break
        while (isSameDay(df.ix[i,'timestamp'],touchReport.ix[c,0])):
            totalTouches[i] += int(touchReport.ix[c,2])
            # Why is this over indexing?
            if c < lengthTouchReport-1:
                c += 1
            else:
                break
    return totalTouches

def appName(subjectID,df,days):
    """calculate the total number of apps opened everyday"""
    appFile = '../CS120/' + subjectID + '/app.csv'
    appReport = csvToDataFrame(appFile)
    # create numpy array to keep track of the total number of touches per day
    totalApps = np.full((days,1),0)
    lengthAppReport = len(appReport)

    c = 0
    # don't count opening apps at the same time
    prevTimestamp = 0
    # loop through the total number of days
    for i in range(days):
        if c == lengthAppReport:
            break
        # i = 52 causes issues
        # add all of the touch events together within the same day
        while (isEarlier(appReport.ix[c,0],df.ix[i,'timestamp'])):
            if c < lengthAppReport-1:
                c += 1
            else:
                break
        while (isSameDay(df.ix[i,'timestamp'],appReport.ix[c,0])):
            if prevTimestamp != appReport.ix[c,0]:
                totalApps[i] += 1
            prevTimestamp = appReport.ix[c,0]
            # Why is this over indexing?
            if c < lengthAppReport-1:
                c += 1
            else:
                break
    return totalApps

def activityType(subjectID,df,days):
    """calculate the percentage of different activity types"""
    actFile = '../CS120/' + subjectID + '/act.csv'
    actReport = csvToDataFrame(actFile)

    featureNames = ['still_perc', 'tilting_perc', 'on_foot_perc', 'in_vehicle_perc', 'biking_perc', 'unknown_perc']
    still_perc = np.zeros((days, 1))
    tilting_perc = np.zeros((days, 1))
    on_foot_perc = np.zeros((days, 1))
    in_vehicle_perc = np.zeros((days, 1))
    biking_perc = np.zeros((days, 1))
    unknown_perc = np.zeros((days, 1))

    lengthActReport = len(actReport)

    c = 0
    # don't count opening apps at the same time
    prevTimestamp = 0
    # loop through the total number of days
    for i in range(days):
        if c == lengthActReport:
            break
        # i = 52 causes issues
        # add all of the touch events together within the same day
        while (isEarlier(actReport.ix[c,0],df.ix[i,'timestamp'])):
            if c < lengthActReport-1:
                c += 1
            else:
                break
        while (isSameDay(df.ix[i,'timestamp'],actReport.ix[c,0])):
            act_type = actReport.ix[c,1]
            if prevTimestamp != actReport.ix[c,0]:
                if act_type == 'STILL':
                    still_perc[i] += 1
                elif act_type == 'TILTING':
                    tilting_perc[i] += 1
                elif act_type == 'ON_FOOT':
                    on_foot_perc[i] += 1
                elif act_type == 'IN_VEHICLE':
                    in_vehicle_perc[i] += 1
                elif act_type == 'ON_BICYCLE':
                    biking_perc[i] += 1
                elif act_type == 'UNKNOWN':
                    unknown_perc[i] += 1
            prevTimestamp = actReport.ix[c,0]
            # Why is this over indexing?
            if c < lengthActReport-1:
                c += 1
            else:
                break

        # Calculate the percentages
        s = still_perc[i]
        t = tilting_perc[i]
        f = on_foot_perc[i]
        v = in_vehicle_perc[i]
        b = biking_perc[i]
        u = unknown_perc[i]
        total = s+t+f+v+b+u

        still_perc[i]= s / total if total > 0 else 0
        tilting_perc[i] = t / total if total > 0 else 0
        on_foot_perc[i] = f / total if total > 0 else 0
        in_vehicle_perc[i] = v / total if total > 0 else 0
        biking_perc[i] = b / total if total > 0 else 0
        unknown_perc[i] = u / total if total > 0 else 0

    return featureNames, [still_perc, tilting_perc, on_foot_perc, in_vehicle_perc, biking_perc,unknown_perc]

def appCategory(subjectID,df,days):
    """calculate the percentage of different app category"""
    appFile = '../CS120/' + subjectID + '/app.csv'
    appReport = csvToDataFrame(appFile)

    featureNames = ['books_perc', 'bundled_perc','bus_perc', 'comics_perc', 'comm_perc', 'ed_perc', 'ent_perc','fin_per','health_per','lib_per','life_perc','media_perc','med_perc','music_perc','news_perc','pers_perc','photo_perc','prod_perc','shop_perc','soc_perc','sports_perc','tools_perc','trans_perc','travel_perc','weather_perc']
    
    books_perc = np.zeros((days, 1))
    bus_perc = np.zeros((days, 1))
    bundled_perc = np.zeros((days, 1))
    comics_perc = np.zeros((days, 1))
    comm_perc = np.zeros((days, 1))
    ed_perc = np.zeros((days, 1))
    ent_perc = np.zeros((days, 1))
    fin_per = np.zeros((days, 1))
    health_per = np.zeros((days, 1))
    lib_per = np.zeros((days, 1))
    life_perc = np.zeros((days, 1))
    media_perc = np.zeros((days, 1))
    med_perc = np.zeros((days, 1))
    music_perc = np.zeros((days, 1))
    news_perc = np.zeros((days, 1))
    pers_perc = np.zeros((days, 1))
    photo_perc = np.zeros((days, 1))
    prod_perc = np.zeros((days, 1))
    shop_perc = np.zeros((days, 1))
    soc_perc = np.zeros((days, 1))
    sports_perc = np.zeros((days, 1))
    tools_perc = np.zeros((days, 1))
    trans_perc = np.zeros((days, 1))
    travel_perc = np.zeros((days, 1))
    weather_perc = np.zeros((days, 1))

    lengthAppReport = len(appReport)

    c = 0
    # don't count opening apps at the same time
    prevTimestamp = 0
    # loop through the total number of days
    for i in range(days):
        if c == lengthAppReport:
            break
        # i = 52 causes issues
        # add all of the touch events together within the same day
        while (isEarlier(appReport.ix[c,0],df.ix[i,'timestamp'])):
            if c < lengthAppReport-1:
                c += 1
            else:
                break
        while (isSameDay(df.ix[i,'timestamp'],appReport.ix[c,0])):
            app_type = appReport.ix[c,3]

            if prevTimestamp != appReport.ix[c,0]:
                if app_type == 'Books & Reference':
                    books_perc[i] += 1
                elif app_type == 'Bundled':
                    bundled_perc[i] += 1
                elif app_type == 'Business':
                    bus_perc[i] += 1
                elif app_type == 'Comics':
                    comics_perc[i] += 1
                elif app_type == 'Communications':
                    comm_perc[i] += 1
                elif app_type == 'Education':
                    ed_perc[i] += 1
                elif app_type == 'Entertainment':
                    ent_perc[i] += 1
                elif app_type == 'Finance':
                    fin_per[i] += 1
                elif app_type == 'Health & Fitness':
                    health_per[i] += 1
                elif app_type == 'Libraries & Demo':
                    lib_per[i] += 1
                elif app_type == 'Lifestyle':
                    life_perc[i] += 1
                elif app_type == 'Media & Video':
                    media_perc[i] += 1
                elif app_type == 'Medical':
                    med_perc[i] += 1
                elif app_type == 'Music & Audio':
                    music_perc[i] += 1
                elif app_type == 'News & Magazines':
                    news_perc[i] += 1
                elif app_type == 'Personalization':
                    pers_perc[i] += 1
                elif app_type == 'Photography':
                    photo_perc[i] += 1
                elif app_type == 'Productivity':
                    prod_perc[i] += 1
                elif app_type == 'Shopping':
                    shop_perc[i] += 1
                elif app_type == 'Social':
                    soc_perc[i] += 1
                elif app_type == 'Sports':
                    sports_perc[i] += 1
                elif app_type == 'Tools':
                    tools_perc[i] += 1
                elif app_type == 'Transportation':
                    trans_perc[i] += 1
                elif app_type == 'Travel & Local':
                    travel_perc[i] += 1
                elif app_type == 'Weather':
                    weather_perc[i] += 1
            prevTimestamp = appReport.ix[c,0]
            # Why is this over indexing?
            if c < lengthAppReport-1:
                c += 1
            else:
                break

        # Calculate the percentages
        b = books_perc[i]
        bun = bundled_perc[i]
        bu = bus_perc[i]
        co = comics_perc[i]
        com = comm_perc[i]
        ed = ed_perc[i]
        ent = ent_perc[i]
        fin = fin_per[i]
        he = health_per[i]
        lib = lib_per[i]
        life = life_perc[i]
        m = media_perc[i]
        med = med_perc[i]
        mus = music_perc[i]
        news = news_perc[i]
        pers = pers_perc[i]
        ph = photo_perc[i]
        pr = prod_perc[i]
        shop = shop_perc[i]
        soc = soc_perc[i]
        sp = sports_perc[i]
        to = tools_perc[i]
        trans = trans_perc[i]
        trav = travel_perc[i]
        w = weather_perc[i]
        total = b + bun + bu + co + com + ed + ent + fin + he + lib + life + m + med + mus + news + pers + ph + pr + shop + soc + sp + to + trans + trav + w

        books_perc[i]= b / total if total > 0 else 0
        bundled_perc[i]= bun / total if total > 0 else 0
        bus_perc[i] = bu / total if total > 0 else 0
        comics_perc[i] = co / total if total > 0 else 0
        comm_perc[i] = com / total if total > 0 else 0
        ed_perc[i] = ed / total if total > 0 else 0
        ent_perc[i] = ent / total if total > 0 else 0
        fin_per[i] = fin / total if total > 0 else 0
        health_per[i] = he / total if total > 0 else 0
        lib_per[i] = lib / total if total > 0 else 0
        life_perc[i] = life / total if total > 0 else 0
        media_perc[i] = m / total if total > 0 else 0
        med_perc[i] = med / total if total > 0 else 0
        music_perc[i]= mus / total if total > 0 else 0
        news_perc[i] = news / total if total > 0 else 0
        pers_perc[i] = pers / total if total > 0 else 0
        photo_perc[i] = ph / total if total > 0 else 0
        prod_perc[i] = pr / total if total > 0 else 0
        shop_perc[i] = shop / total if total > 0 else 0
        soc_perc[i] = soc / total if total > 0 else 0
        sports_perc[i] = sp / total if total > 0 else 0
        tools_perc[i] = to / total if total > 0 else 0
        trans_perc[i] = trans / total if total > 0 else 0
        travel_perc[i] = trav / total if total > 0 else 0
        weather_perc[i] = w / total if total > 0 else 0

    return featureNames, [books_perc, bundled_perc, bus_perc, comics_perc, comm_perc, ed_perc, ent_perc, fin_per, health_per, lib_per, life_perc, media_perc, med_perc, music_perc, news_perc, pers_perc, photo_perc, prod_perc, shop_perc, soc_perc, sports_perc, tools_perc, trans_perc, travel_perc, weather_perc]

def runningApps(subjectID,df,days):
    """calculate the mean number of apps running at a given time each day"""
    runFile = '../CS120/' + subjectID + '/run.csv'
    runReport = csvToDataFrame(runFile)
    # create numpy array to keep track of the total number of touches per day
    meanApps = np.full((days,1),0)
    lengthRunReport = len(runReport)

    c = 0
    # don't count opening apps at the same time
    prevTimestamp = 0
    # loop through the total number of days
    for i in range(days):
        # keep track of the number of times the number of running apps is collected
        instances = 0
        if c == lengthRunReport:
            break
        # i = 52 causes issues
        # add all of the touch events together within the same day
        while (isEarlier(runReport.ix[c,0],df.ix[i,'timestamp'])):
            if c < lengthRunReport-1:
                c += 1
            else:
                break
        while (isSameDay(df.ix[i,'timestamp'],runReport.ix[c,0])):
            if prevTimestamp != runReport.ix[c,0]:
                # print(runReport.ix[c,3])
                meanApps[i] += int(runReport.ix[c,3])
                instances += 1
            prevTimestamp = runReport.ix[c,0]
            # Why is this over indexing?
            if c < lengthRunReport-1:
                c += 1
            else:
                break
        meanApps[i] = round(float(meanApps[i])/float(instances)) if instances > 0 else 0
    return meanApps

###################################################################################################################
def weightedActivityType(subjectID,df,days):
    """calculate the weighted percentage of different activity types"""
    actFile = '../CS120/' + subjectID + '/act.csv'
    actReport = csvToDataFrame(actFile)

    featureNames = ['w_still_perc', 'w_tilting_perc', 'w_on_foot_perc', 'w_in_vehicle_perc', 'w_biking_perc', 'w_unknown_perc']
    w_still_perc = np.zeros((days, 1))
    w_tilting_perc = np.zeros((days, 1))
    w_on_foot_perc = np.zeros((days, 1))
    w_in_vehicle_perc = np.zeros((days, 1))
    w_biking_perc = np.zeros((days, 1))
    w_unknown_perc = np.zeros((days, 1))

    lengthActReport = len(actReport)

    c = 0
    # don't count opening apps at the same time
    prevTimestamp = 0
    # loop through the total number of days
    for i in range(days):
        if c == lengthActReport:
            break
        # i = 52 causes issues
        # add all of the touch events together within the same day
        while (isEarlier(actReport.ix[c,0],df.ix[i,'timestamp'])):
            if c < lengthActReport-1:
                c += 1
            else:
                break
        while (isSameDay(df.ix[i,'timestamp'],actReport.ix[c,0])):
            act_type = actReport.ix[c,1]
            if prevTimestamp != actReport.ix[c,0]:
                weight = float(actReport.ix[c,2])/100
                if act_type == 'STILL':
                    w_still_perc[i] += weight
                elif act_type == 'TILTING':
                    w_tilting_perc[i] += weight
                elif act_type == 'ON_FOOT':
                    w_on_foot_perc[i] += weight
                elif act_type == 'IN_VEHICLE':
                    w_in_vehicle_perc[i] += weight
                elif act_type == 'ON_BICYCLE':
                    w_biking_perc[i] += weight
                elif act_type == 'UNKNOWN':
                    w_unknown_perc[i] += weight
            prevTimestamp = actReport.ix[c,0]
            # Why is this over indexing?
            if c < lengthActReport-1:
                c += 1
            else:
                break

        # Calculate the percentages
        s = w_still_perc[i]
        t = w_tilting_perc[i]
        f = w_on_foot_perc[i]
        v = w_in_vehicle_perc[i]
        b = w_biking_perc[i]
        u = w_unknown_perc[i]
        total = s+t+f+v+b+u

        w_still_perc[i]= s / total if total > 0 else 0
        w_tilting_perc[i] = t / total if total > 0 else 0
        w_on_foot_perc[i] = f / total if total > 0 else 0
        w_in_vehicle_perc[i] = v / total if total > 0 else 0
        w_biking_perc[i] = b / total if total > 0 else 0
        w_unknown_perc[i] = u / total if total > 0 else 0

    return featureNames, [w_still_perc, w_tilting_perc, w_on_foot_perc, w_in_vehicle_perc, w_biking_perc,w_unknown_perc]

def appCategoryTotal(subjectID,df,days):
    """calculate the total times each app category is opened"""
    appFile = '../CS120/' + subjectID + '/app.csv'
    appReport = csvToDataFrame(appFile)

    featureNames = ['books_total', 'bundled_total','bus_total', 'comics_total', 'comm_total', 'ed_total', 'ent_total','fin_total','health_total','lib_total','life_total','media_total','med_total','music_total','news_total','pers_total','photo_total','prod_total','shop_total','soc_total','sports_total','tools_total','trans_total','travel_total','weather_total']
    
    books_total = np.zeros((days, 1))
    bus_total = np.zeros((days, 1))
    bundled_total = np.zeros((days, 1))
    comics_total = np.zeros((days, 1))
    comm_total = np.zeros((days, 1))
    ed_total = np.zeros((days, 1))
    ent_total = np.zeros((days, 1))
    fin_total = np.zeros((days, 1))
    health_total = np.zeros((days, 1))
    lib_total = np.zeros((days, 1))
    life_total = np.zeros((days, 1))
    media_total = np.zeros((days, 1))
    med_total = np.zeros((days, 1))
    music_total = np.zeros((days, 1))
    news_total = np.zeros((days, 1))
    pers_total = np.zeros((days, 1))
    photo_total = np.zeros((days, 1))
    prod_total = np.zeros((days, 1))
    shop_total = np.zeros((days, 1))
    soc_total = np.zeros((days, 1))
    sports_total = np.zeros((days, 1))
    tools_total = np.zeros((days, 1))
    trans_total = np.zeros((days, 1))
    travel_total = np.zeros((days, 1))
    weather_total = np.zeros((days, 1))

    lengthAppReport = len(appReport)

    c = 0
    # don't count opening apps at the same time
    prevTimestamp = 0
    # loop through the total number of days
    for i in range(days):
        if c == lengthAppReport:
            break
        # i = 52 causes issues
        # add all of the touch events together within the same day
        while (isEarlier(appReport.ix[c,0],df.ix[i,'timestamp'])):
            if c < lengthAppReport-1:
                c += 1
            else:
                break
        while (isSameDay(df.ix[i,'timestamp'],appReport.ix[c,0])):
            app_type = appReport.ix[c,3]

            if prevTimestamp != appReport.ix[c,0]:
                if app_type == 'Books & Reference':
                    books_total[i] += 1
                elif app_type == 'Bundled':
                    bundled_total[i] += 1
                elif app_type == 'Business':
                    bus_total[i] += 1
                elif app_type == 'Comics':
                    comics_total[i] += 1
                elif app_type == 'Communications':
                    comm_total[i] += 1
                elif app_type == 'Education':
                    ed_total[i] += 1
                elif app_type == 'Entertainment':
                    ent_total[i] += 1
                elif app_type == 'Finance':
                    fin_total[i] += 1
                elif app_type == 'Health & Fitness':
                    health_total[i] += 1
                elif app_type == 'Libraries & Demo':
                    lib_total[i] += 1
                elif app_type == 'Lifestyle':
                    life_total[i] += 1
                elif app_type == 'Media & Video':
                    media_total[i] += 1
                elif app_type == 'Medical':
                    med_total[i] += 1
                elif app_type == 'Music & Audio':
                    music_total[i] += 1
                elif app_type == 'News & Magazines':
                    news_total[i] += 1
                elif app_type == 'Personalization':
                    pers_total[i] += 1
                elif app_type == 'Photography':
                    photo_total[i] += 1
                elif app_type == 'Productivity':
                    prod_total[i] += 1
                elif app_type == 'Shopping':
                    shop_total[i] += 1
                elif app_type == 'Social':
                    soc_total[i] += 1
                elif app_type == 'Sports':
                    sports_total[i] += 1
                elif app_type == 'Tools':
                    tools_total[i] += 1
                elif app_type == 'Transportation':
                    trans_total[i] += 1
                elif app_type == 'Travel & Local':
                    travel_total[i] += 1
                elif app_type == 'Weather':
                    weather_total[i] += 1
            prevTimestamp = appReport.ix[c,0]
            # Why is this over indexing?
            if c < lengthAppReport-1:
                c += 1
            else:
                break

    return featureNames, [books_total, bundled_total, bus_total, comics_total, comm_total, ed_total, ent_total, fin_total, health_total, lib_total, life_total, media_total, med_total, music_total, news_total, pers_total, photo_total, prod_total, shop_total, soc_total, sports_total, tools_total, trans_total, travel_total, weather_total]

def runningAppsMaxMin(subjectID,df,days):
    """calculate the max and min number of apps running at a given time each day"""
    runFile = '../CS120/' + subjectID + '/run.csv'
    runReport = csvToDataFrame(runFile)
    # create numpy array to keep track of the total number of touches per day
    featureNames = ['maxApps','minApps']
    maxApps = np.full((days,1),0)
    minApps = np.full((days,1),0)
    lengthRunReport = len(runReport)

    c = 0
    # don't count opening apps at the same time
    prevTimestamp = 0
    # loop through the total number of days
    for i in range(days):
        tempArr = []
        # keep track of the number of times the number of running apps is collected
        instances = 0
        if c == lengthRunReport:
            break
        # i = 52 causes issues
        # add all of the touch events together within the same day
        while (isEarlier(runReport.ix[c,0],df.ix[i,'timestamp'])):
            if c < lengthRunReport-1:
                c += 1
            else:
                break
        while (isSameDay(df.ix[i,'timestamp'],runReport.ix[c,0])):
            if prevTimestamp != runReport.ix[c,0]:
                # print(runReport.ix[c,3])
                tempArr.append(runReport.ix[c,3])
            prevTimestamp = runReport.ix[c,0]
            # Why is this over indexing?
            if c < lengthRunReport-1:
                c += 1
            else:
                break
        if (len(tempArr) > 0):
            maxApps[i] = max(tempArr)
            minApps[i] = min(tempArr)
        else:
            maxApps[i] = 0
            minApps[i] = 0

    return featureNames, [maxApps,minApps]

def activityTypeTime(subjectID,df,days):
    """calculate the total, min, and max time spent in each activity type"""
    actFile = '../CS120/' + subjectID + '/act.csv'
    actReport = csvToDataFrame(actFile)

    featureNames = ['total_still_time','max_still_time','min_still_time', 'total_tilting_time','max_tilting_time','min_tilting_time', 'total_on_foot_time','max_on_foot_time','min_on_foot_time', 'total_in_vehicle_time','max_in_vehicle_time','min_in_vehicle_time', 'total_biking_time','max_biking_time','min_biking_time', 'total_unknown_time','max_unknown_time','min_unknown_time']
    total_still_time = np.zeros((days, 1))
    max_still_time = np.zeros((days, 1))
    min_still_time = np.zeros((days, 1))
    total_tilting_time = np.zeros((days, 1))
    max_tilting_time = np.zeros((days, 1))
    min_tilting_time = np.zeros((days, 1))
    total_on_foot_time = np.zeros((days, 1))
    max_on_foot_time = np.zeros((days, 1))
    min_on_foot_time = np.zeros((days, 1))
    total_in_vehicle_time = np.zeros((days, 1))
    max_in_vehicle_time = np.zeros((days, 1))
    min_in_vehicle_time = np.zeros((days, 1))
    total_on_bicycle_time = np.zeros((days, 1))
    max_on_bicycle_time = np.zeros((days, 1))
    min_on_bicycle_time = np.zeros((days, 1))
    total_unknown_time = np.zeros((days, 1))
    max_unknown_time = np.zeros((days, 1))
    min_unknown_time = np.zeros((days, 1))

    lengthActReport = len(actReport)

    c = 0
    # don't count opening apps at the same time
    prevTimestamp = 0
    # loop through the total number of days
    for i in range(days):
        tempDict = {'STILL': [], 'TILTING': [], 'ON_FOOT': [], 'IN_VEHICLE': [], 'ON_BICYCLE': [], 'UNKNOWN': []}
        if c == lengthActReport:
            break
        # i = 52 causes issues
        # add all of the touch events together within the same day
        while (isEarlier(actReport.ix[c,0],df.ix[i,'timestamp'])):
            if c < lengthActReport-1:
                c += 1
            else:
                break
        # Initialize the previous type to compare against
        # check the type of the timestamp!!!!
        # to keep track of the first instance the type is seen
        recent_act = [actReport.ix[c,0],actReport.ix[c,1]]
        # to keep track of the previous value
        prev_act = [actReport.ix[c,0],actReport.ix[c,1]]
        while (isSameDay(df.ix[i,'timestamp'],actReport.ix[c,0])):
            act = [actReport.ix[c,0],actReport.ix[c,1]]
            if act[1] != recent_act[1]:
                tempDict[prev_act[1]].append(float(prev_act[0])-float(recent_act[0]))
                recent_act = act
            prev_act = act
            # Why is this over indexing?
            if c < lengthActReport-1:
                c += 1
            else:
                break

        total_still_time[i] = sum(tempDict['STILL']) if len(tempDict['STILL']) > 0 else 0
        max_still_time[i] = max(tempDict['STILL']) if len(tempDict['STILL']) > 0 else 0
        min_still_time[i] = min(tempDict['STILL']) if len(tempDict['STILL']) > 0 else 0
        total_tilting_time[i] = sum(tempDict['TILTING']) if len(tempDict['TILTING']) > 0 else 0
        max_tilting_time[i] = max(tempDict['TILTING']) if len(tempDict['TILTING']) > 0 else 0
        min_tilting_time[i] = min(tempDict['TILTING']) if len(tempDict['TILTING']) > 0 else 0
        total_on_foot_time[i] = sum(tempDict['ON_FOOT']) if len(tempDict['ON_FOOT']) > 0 else 0
        max_on_foot_time[i] = max(tempDict['ON_FOOT']) if len(tempDict['ON_FOOT']) > 0 else 0
        min_on_foot_time[i] = min(tempDict['ON_FOOT']) if len(tempDict['ON_FOOT']) > 0 else 0
        total_in_vehicle_time[i] = sum(tempDict['IN_VEHICLE']) if len(tempDict['IN_VEHICLE']) > 0 else 0
        max_in_vehicle_time[i] = max(tempDict['IN_VEHICLE']) if len(tempDict['IN_VEHICLE']) > 0 else 0
        min_in_vehicle_time[i] = min(tempDict['IN_VEHICLE']) if len(tempDict['IN_VEHICLE']) > 0 else 0
        total_on_bicycle_time[i] = sum(tempDict['ON_BICYCLE']) if len(tempDict['ON_BICYCLE']) > 0 else 0
        max_on_bicycle_time[i] = max(tempDict['ON_BICYCLE']) if len(tempDict['ON_BICYCLE']) > 0 else 0
        min_on_bicycle_time[i] = min(tempDict['ON_BICYCLE']) if len(tempDict['ON_BICYCLE']) > 0 else 0
        total_unknown_time[i] = sum(tempDict['UNKNOWN']) if len(tempDict['UNKNOWN']) > 0 else 0
        max_unknown_time[i] = max(tempDict['UNKNOWN']) if len(tempDict['UNKNOWN']) > 0 else 0
        min_unknown_time[i] = min(tempDict['UNKNOWN']) if len(tempDict['UNKNOWN']) > 0 else 0

    return featureNames, [total_still_time, max_still_time, min_still_time, total_tilting_time, max_tilting_time, min_tilting_time, total_on_foot_time, max_on_foot_time, min_on_foot_time, total_in_vehicle_time, max_in_vehicle_time, min_in_vehicle_time, total_on_bicycle_time, max_on_bicycle_time, min_on_bicycle_time, total_unknown_time, max_unknown_time, min_unknown_time]

def appTime(subjectID,df,days):
    """calculate the mean, min, and max time between opening apps"""
    appFile = '../CS120/' + subjectID + '/app.csv'
    appReport = csvToDataFrame(appFile)

    featureNames = ['min_time_apps','max_time_apps','mean_time_apps']
    min_time_apps = np.zeros((days, 1))
    max_time_apps = np.zeros((days, 1))
    mean_time_apps = np.zeros((days, 1))

    lengthAppReport = len(appReport)

    c = 0
    # don't count opening apps at the same time
    prevTimestamp = 0
    # loop through the total number of days
    for i in range(days):
        tempTime = []
        if c == lengthAppReport:
            break
        # i = 52 causes issues
        # add all of the touch events together within the same day
        while (isEarlier(appReport.ix[c,0],df.ix[i,'timestamp'])):
            if c < lengthAppReport-1:
                c += 1
            else:
                break
        # Initialize the previous type to compare against
        # check the type of the timestamp!!!!
        # to keep track of the previous value
        prev_time = float(appReport.ix[c,0])
        while (isSameDay(df.ix[i,'timestamp'],appReport.ix[c,0])):
            curr_time = float(appReport.ix[c,0])
            if prev_time != curr_time:
                tempTime.append(curr_time-prev_time)
                prev_time = curr_time
            # Why is this over indexing?
            if c < lengthAppReport-1:
                c += 1
            else:
                break

        min_time_apps[i] = min(tempTime) if len(tempTime) > 0 else 0
        max_time_apps[i] = max(tempTime) if len(tempTime) > 0 else 0
        mean_time_apps[i] = sum(tempTime)/len(tempTime) if len(tempTime) > 0 else 0

    return featureNames, [min_time_apps,max_time_apps,mean_time_apps]

def createBigCSV(path_to_directory):
    """main function that compiles all calculated features into an excel spreadsheet"""
    participantIDs = getDirNames(path_to_directory)
    print(participantIDs)
    for Id in participantIDs:
        try:
            labels = labelEachDay(Id)
        except:
            print("ems.csv doesn't exist for " + Id)
            continue
        labels['day'] = np.arange(1,len(labels)+1)
        labels['id'] = Id
        days = len(labels)
        print("Id " + str(Id))
        # # total number of times someone touches their phone everyday
        # try:
        #     totalTouches = touchEvents(Id,labels,days)   
        # except:
        #     print("tch.csv doesn't exist for " + Id)
        #     totalTouches = np.full((days,1),-1)
        # labels['num_touches'] = totalTouches

        # # total number of apps someone opens in a day
        # try:
        #     totalApps = appName(Id,labels,days)   
        # except:
        #     print("app.csv doesn't exist for " + Id)
        #     totalApps = np.full((days,1),-1)
        # labels['total_apps'] = totalApps

        # percentage of each type of activity per day
        featureNames = ['still_perc', 'tilting_perc', 'on_foot_perc', 'in_vehicle_perc', 'biking_perc', 'unknown_perc']
        activityPercentages = [0]* len(featureNames)
        try:
            featureNames, activityPercentages = activityType(Id,labels,days)   
        except:
            print("act.csv doesn't exist for " + Id)
            for i in range(len(featureNames)):
                labels[activityPercentages[i]] = np.full((days,1),-1)
        for i in range(len(featureNames)):
            labels[featureNames[i]] = activityPercentages[i]

        # # percentage of each type of app category used per day
        # featureNames = ['books_perc','bundled_perc' ,'bus_perc', 'comics_perc', 'comm_perc', 'ed_perc', 'ent_perc','fin_per','health_per','lib_per','life_perc','media_perc','med_perc','music_perc','news_perc','pers_perc','photo_perc','prod_perc','shop_perc','soc_perc','sports_perc','tools_perc','trans_perc','travel_perc','weather_perc']
        # appPercentages = [0]*len(featureNames)
        # try:
        #     featureNames, appPercentages = appCategory(Id,labels,days)   
        # except:
        #     print("app.csv doesn't exist for " + Id)
        #     # there are 24 feature names
        #     for i in range(len(featureNames)):
        #         appPercentages[i] = np.full((days,1),-1) 
        # for i in range(len(featureNames)):
        #     labels[featureNames[i]] = appPercentages[i]

        # # mean number of apps running at a given time each day
        # try:
        #     meanApps = runningApps(Id,labels,days)   
        # except:
        #     print("run.csv doesn't exist for " + Id)
        #     meanApps = np.full((days,1),-1)
        # labels['mean_apps'] = meanApps

        ##################################################
        # weighted percentage of each type of activity per day
        featureNames = ['w_still_perc', 'w_tilting_perc', 'w_on_foot_perc', 'w_in_vehicle_perc', 'w_biking_perc', 'w_unknown_perc']
        activityPercentages = [0]* len(featureNames)
        try:
            featureNames, activityPercentages = weightedActivityType(Id,labels,days)   
        except:
            print("act.csv doesn't exist for " + Id)
            for i in range(len(featureNames)):
                labels[activityPercentages[i]] = np.full((days,1),-1)
        for i in range(len(featureNames)):
            labels[featureNames[i]] = activityPercentages[i]

        # percentage of each type of app category used per day
        featureNames = ['books_total', 'bundled_total','bus_total', 'comics_total', 'comm_total', 'ed_total', 'ent_total','fin_total','health_total','lib_total','life_total','media_total','med_total','music_total','news_total','pers_total','photo_total','prod_total','shop_total','soc_total','sports_total','tools_total','trans_total','travel_total','weather_total']
        appPercentages = [0]*len(featureNames)
        try:
            featureNames, appPercentages = appCategoryTotal(Id,labels,days)   
        except:
            print("app.csv doesn't exist for " + Id)
            # there are 24 feature names
            for i in range(len(featureNames)):
                appPercentages[i] = np.full((days,1),-1) 
        for i in range(len(featureNames)):
            labels[featureNames[i]] = appPercentages[i]

        # percentage of each type of app category used per day
        featureNames = ['maxApps','minApps']
        appPercentages = [0]*len(featureNames)
        try:
            featureNames, appPercentages = runningAppsMaxMin(Id,labels,days)   
        except:
            print("app.csv doesn't exist for " + Id)
            # there are 24 feature names
            for i in range(len(featureNames)):
                appPercentages[i] = np.full((days,1),-1) 
        for i in range(len(featureNames)):
            labels[featureNames[i]] = appPercentages[i]

        # weighted percentage of each type of activity per day
        featureNames = ['total_still_time','max_still_time','min_still_time', 'total_tilting_time','max_tilting_time','min_tilting_time', 'total_on_foot_time','max_on_foot_time','min_on_foot_time', 'total_in_vehicle_time','max_in_vehicle_time','min_in_vehicle_time', 'total_biking_time','max_biking_time','min_biking_time', 'total_unknown_time','max_unknown_time','min_unknown_time']
        activityPercentages = [0]* len(featureNames)
        try:
            featureNames, activityPercentages = activityTypeTime(Id,labels,days)   
        except:
            print("act.csv doesn't exist for " + Id)
            for i in range(len(featureNames)):
                labels[activityPercentages[i]] = np.full((days,1),-1)
        for i in range(len(featureNames)):
            labels[featureNames[i]] = activityPercentages[i]

        # min/max/mean time between opening apps
        featureNames = ['min_time_apps','max_time_apps','mean_time_apps']
        activityPercentages = [0]* len(featureNames)
        try:
            eatureNames, activityPercentages = appTime(Id,labels,days)   
        except:
            print("app.csv doesn't exist for " + Id)
            for i in range(len(featureNames)):
                labels[activityPercentages[i]] = np.full((days,1),-1)
        for i in range(len(featureNames)):
            labels[featureNames[i]] = activityPercentages[i]

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

def reduceFileSize(path_to_file):
    """Create a smaller file for testing"""
    data = csv.reader(open(path_to_file, 'r'))
    writer = csv.writer(open('/Users/morganwalker/Desktop/Winter 2017/mHealth/Depression Data/CS120/62977/runReduced.csv', 'w'))
    counter = 1
    for row in data:
        if counter%1501 == 0:
            writer.writerow(row)
        counter += 1
    print("Success")


createBigCSV("/Users/morganwalker/Desktop/Winter 2017/mHealth/Depression Data/CS120")
# print(isSameDay("1448387135.0","1448333696.0"))
# reduceFileSize("/Users/morganwalker/Desktop/Winter 2017/mHealth/Depression Data/CS120/62977/run.csv")

