####### SOPHIA'S CODE #####################################################################################

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

#inputs are strings
def isEarlier(sensor_ts,day_ts):
    if '"' in sensor_ts:
        sensor_ts = sensor_ts.replace('"','')
    if '"' in day_ts:
        day_ts = day_ts.replace('"', '')
    return float(sensor_ts) < float(day_ts)

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

    for i in range(len(wifiReport)):
        ts = wifiReport[0][i]
        accessPoints = float(wifiReport[3][i])

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


###################### RYAN'S CODE #######################################################################

################ screen state ############################################

def screenStateFeatures():
    participantIDs = getDirNames('../CS120/')
    
    screenFeatures = pd.DataFrame()

    person_count = 0
    
    for Id in participantIDs:
        
        f = labelEachDay(Id)
        f['day'] = np.arange(1,len(f)+1)
        f['id'] = Id;        
        
        screenFile = '../CS120/' + Id + '/scr.csv'
        if (os.path.isfile(screenFile)):
            screenData = csvToDataFrame(screenFile)
        else:
            f['num_screen_changes'] = -1
            screenFeatures = pd.concat([screenFeatures, f])
            continue         
        
        if (screenFeatures is None):
            screenFeatures = calcScreenStateFeatures(Id,f,screenData)
        else:
            screenFeatures = pd.concat([screenFeatures, calcScreenStateFeatures(Id,f,screenData)])
        
        person_count += 1
        print 'Have processed %d people for screen features' %person_count

        # break to test after one person
        #break


        
    screenFeatures.to_csv('screenFeatures.csv', index=False)
    return screenFeatures


def calcScreenStateFeatures(Id,f,screenData):
    
    f['num_screen_changes'] = 0.0
    
    days = f.shape[0]
    index = 0
    # loop through rows of screenData 
    for i in range(screenData.shape[0]):
        row_ts = screenData.iloc[i,0]
        
        while(index < days):
            day_ts = f.iloc[index,0]
            if isSameDay(row_ts,day_ts):
                # num_screen_changes
                f.iloc[index,4] += 1 
                break
            elif isEarlier(row_ts, day_ts):
                break
            index += 1

        '''
        # overly complex way
        # loop through day numbers 
        for j in range(f.shape[0]):
            day_ts = f.iloc[j,0]
            if isSameDay(row_ts,day_ts):
                
                # num_screen_changes
                f.iloc[j,4] += 1 
        ''' 
        
    return f


################ call state #################################################

def callStateFeatures():
    participantIDs = getDirNames('../CS120/')
    
    callStateFeatures = pd.DataFrame()

    person_count = 0
    
    for Id in participantIDs:
        
        f = labelEachDay(Id)
        f['day'] = np.arange(1,len(f)+1)
        f['id'] = Id;        
        
        callFile = '../CS120/' + Id + '/cal.csv'
        if (os.path.isfile(callFile)):
            callData = csvToDataFrame(callFile)
        else:
            f['times_idle'] = -1
            f['times_ringing'] = -1
            f['times_offhook'] = -1
            callStateFeatures = pd.concat([callStateFeatures, f])
            continue 
        
        if (callStateFeatures is None):
            callStateFeatures = calcCallFeatures(Id,f,callData)
        else:
            callStateFeatures = pd.concat([callStateFeatures, calcCallFeatures(Id,f,callData)])

        person_count += 1
        print 'Have processed %d people for call state features' %person_count
        
        # break to test after one person
        #break
        
    callStateFeatures.to_csv('callFeatures.csv', index=False)
    return callStateFeatures

def calcCallFeatures(Id,f,callData):
    
    f['times_idle'] = 0.0
    f['times_ringing'] = 0.0
    f['times_offhook'] = 0.0

    days = f.shape[0]
    index = 0
    
    for i in range(callData.shape[0]):
        row_ts = callData.iloc[i,0]
        # loop through day numbers 
        
        while(index < days):
            day_ts = f.iloc[index,0]
            if isSameDay(row_ts,day_ts):
                
                # times_idle
                if (callData.iloc[i,1] == 'Idle'):
                    f.iloc[index,4] += 1
                
                # times_ringing
                if (callData.iloc[i,1] == 'Ringing'):
                    f.iloc[index,5] += 1
                
                # times_offhook
                if (callData.iloc[i,1] == 'Off-Hook'):
                    f.iloc[index,6] += 1 

                break
            elif isEarlier(row_ts,day_ts):
                break
            index += 1

        '''
        for j in range(f.shape[0]):
            day_ts = f.iloc[j,0]
            if isSameDay(row_ts,day_ts):
                
                # times_idle
                if (callData.iloc[i,1] == 'Idle'):
                    f.iloc[j,4] += 1
                
                # times_ringing
                if (callData.iloc[i,1] == 'Ringing'):
                    f.iloc[j,5] += 1
                
                # times_offhook
                if (callData.iloc[i,1] == 'Off-Hook'):
                    f.iloc[j,6] += 1 
        '''

    return f


################ GPS location #################################################
    
def locationFeatures():
    participantIDs = getDirNames('../CS120/')
    
    locationFeatures = pd.DataFrame()

    person_count = 0
    
    for Id in participantIDs:
        
        f = labelEachDay(Id)
        f['day'] = np.arange(1,len(f)+1)
        f['id'] = Id;        
        
        locationFile = '../CS120/' + Id + '/fus.csv'
        if (os.path.isfile(locationFile)):
            locationData = csvToDataFrame(locationFile)
        else:
            f['mean_altitude'] = -1
            locationFeatures = pd.concat([locationFeatures, f])
            continue 
        
        if (locationFeatures is None):
            locationFeatures = mean_altitude(Id,f,locationData)
        else:
            locationFeatures = pd.concat([locationFeatures, mean_altitude(Id,f,locationData)])
        
        person_count += 1
        print 'Have processed %d people for location features' %person_count

        # break to test after one person
        #break
        
    locationFeatures.to_csv('locationFeatures.csv', index=False)
    return locationFeatures

# mean altitude through the day
def mean_altitude(Id,f,locationData):
    
    f['mean_altitude'] = 0.0

    days = f.shape[0]
    index = 0
    
    for i in range(locationData.shape[0]):
        row_ts = locationData.iloc[i,0]
        # loop through day numbers 

        while (index < days):
            day_ts = f.iloc[index,0]
            if isSameDay(row_ts,day_ts):
                if (f.iloc[index,4] == 0.0):
                    f.iloc[index,4] = float(locationData.iloc[i,3])
                else:
                    f.iloc[index,4] = (f.iloc[index,4] + float(locationData.iloc[i,3])) / 2
                break
            elif(isEarlier(row_ts,day_ts)):
                break
            index += 1

        '''
        for j in range(f.shape[0]):
            day_ts = f.iloc[j,0]
            if isSameDay(row_ts,day_ts):
                if (f.iloc[j,4] == 0.0):
                    f.iloc[j,4] = float(locationData.iloc[i,3])
                else:
                    f.iloc[j,4] = (f.iloc[j,4] + float(locationData.iloc[i,3])) / 2
        '''
    
                
    return f
    
    
################ sound #################################################

def soundFeatures():
    participantIDs = getDirNames('../CS120/')
                
    soundFeatures = pd.DataFrame()

    person_count = 0
    
    for Id in participantIDs:
        
        f = labelEachDay(Id)
        f['day'] = np.arange(1,len(f)+1)
        f['id'] = Id;

        soundFile = '../CS120/' + Id + '/aud.csv'
        if (os.path.isfile(soundFile)):
            soundData = csvToDataFrame(soundFile)
        else:
            f['total_norm_pow'] = -1
            f['max_norm_pow'] = -1
            f['min_norm_pow'] = -1
            f['mean_dom_freq'] = -1
            f['max_dom_freq'] = -1
            f['min_dom_freq'] = -1
            f['total_norm_amp'] = -1
            soundFeatures = pd.concat([soundFeatures, f])
            continue

        # need to concatenate the next dataframe
        if (soundFeatures is None):
            soundFeatures = calcSoundFeatures(Id,f,soundData)
        else:
            soundFeatures = pd.concat([soundFeatures, calcSoundFeatures(Id,f,soundData)])
        
        person_count += 1
        print 'Have processed %d people for sound features' %person_count

        # break to test on just one person
        #break

        
    soundFeatures.to_csv('soundFeatures.csv', index=False)
    return soundFeatures
 

def calcSoundFeatures(Id,f,soundData):
    
    f['total_norm_pow'] = 0.0
    f['max_norm_pow'] = 0.0
    f['min_norm_pow'] = float("inf")
    f['mean_dom_freq'] = 0.0
    f['max_dom_freq'] = 0.0
    f['min_dom_freq'] = float("inf")
    f['total_norm_amp'] = 0.0

    days = f.shape[0]
    index = 0
    
    for i in range(soundData.shape[0]):
        row_ts = soundData.iloc[i,0]
        # loop through day numbers 

        while(index < days):
            day_ts = f.iloc[index,0]
            if isSameDay(row_ts,day_ts):
                
                # total_norm_pow
                f.iloc[index,4] += float(soundData.iloc[i,1])
                
                # max_norm_pow
                if (float(soundData.iloc[i,1]) > f.iloc[index,5]):
                    f.iloc[index,5] = float(soundData.iloc[i,1])
                    
                # min_norm_pow
                if (float(soundData.iloc[i,1]) < f.iloc[index,6] and (float(soundData.iloc[i,1]) != 0.0)):
                    f.iloc[index,6] = float(soundData.iloc[i,1]) 
                    
                # mean_dom_freq
                if (f.iloc[index,7] == 0.0):
                    f.iloc[index,7] = float(soundData.iloc[i,2])
                else:
                    f.iloc[index,7] = (f.iloc[index,7] + float(soundData.iloc[i,1])) / 2
                    
                # max_dom_freq
                if (float(soundData.iloc[i,2]) > f.iloc[index,8]):
                    f.iloc[index,8] = float(soundData.iloc[i,2])
                
                # min_dom_freq
                if (float(soundData.iloc[i,2]) < f.iloc[index,9] and (float(soundData.iloc[i,2]) != 0.0)):
                    f.iloc[index,9] = float(soundData.iloc[i,2]) 
                
                # total_norm_amp
                f.iloc[index,10] += float(soundData.iloc[i,3])

                break
            elif (isEarlier(row_ts,day_ts)):
                break
            index += 1

        
        '''
        for j in range(f.shape[0]):
            day_ts = f.iloc[j,0]
            if isSameDay(row_ts,day_ts):
                
                # total_norm_pow
                f.iloc[j,4] += float(soundData.iloc[i,1])
                
                # max_norm_pow
                if (float(soundData.iloc[i,1]) > f.iloc[j,5]):
                    f.iloc[j,5] = float(soundData.iloc[i,1])
                    
                # min_norm_pow
                if (float(soundData.iloc[i,1]) < f.iloc[j,6] and (float(soundData.iloc[i,1]) != 0.0)):
                    f.iloc[j,6] = float(soundData.iloc[i,1]) 
                    
                # mean_dom_freq
                if (f.iloc[j,7] == 0.0):
                    f.iloc[j,7] = float(soundData.iloc[i,2])
                else:
                    f.iloc[j,7] = (f.iloc[j,7] + float(soundData.iloc[i,1])) / 2
                    
                # max_dom_freq
                if (float(soundData.iloc[i,2]) > f.iloc[j,8]):
                    f.iloc[j,8] = float(soundData.iloc[i,2])
                
                # min_dom_freq
                if (float(soundData.iloc[i,2]) < f.iloc[j,9] and (float(soundData.iloc[i,2]) != 0.0)):
                    f.iloc[j,9] = float(soundData.iloc[i,2]) 
                
                # total_norm_amp
                f.iloc[j,10] += float(soundData.iloc[i,3])
        '''
                
    return f



######################## writing affect features to predict ##############################
def stressOutcome():
    participantIDs = getDirNames('../CS120/')
    stressFeature = pd.DataFrame()
    person_count = 0
    
    for Id in participantIDs:
        
        f = labelEachDay(Id)
        f['day'] = np.arange(1,len(f)+1)
        f['id'] = Id;        
        
        affectFile = '../CS120/' + Id + '/emm.csv'
        if (os.path.isfile(affectFile)):
            affectData = csvToDataFrame(affectFile)
        else:
            f['stress'] = -1
            stressFeature = pd.concat([stressFeature, f])
            continue 
        
        if (stressFeature is None):
            stressFeature = calcStress(Id,f,affectData)
        else:
            stressFeature = pd.concat([stressFeature, calcStress(Id,f,affectData)])
        
        person_count += 1
        print 'Have processed %d people for stress feature' %person_count
        
    stressFeature.to_csv('stressFeature.csv', index=False)
    return stressFeature


def calcStress(Id,f,affectData):

    f['stress'] = 0.0

    for i in range((affectData.shape[0])/3):

        if (i == f.shape[0]):
            break

        j = i * 3
        todays_stress = affectData.iloc[j,1] + affectData.iloc[j+1,1] + affectData.iloc[j+2,1]

        f.iloc[i,4] = todays_stress

    return f

def moodOutcome():
    participantIDs = getDirNames('../CS120/')
    moodFeature = pd.DataFrame()
    person_count = 0
    
    for Id in participantIDs:
        
        f = labelEachDay(Id)
        f['day'] = np.arange(1,len(f)+1)
        f['id'] = Id;        
        
        affectFile = '../CS120/' + Id + '/emm.csv'
        if (os.path.isfile(affectFile)):
            affectData = csvToDataFrame(affectFile)
        else:
            f['mood'] = -1
            moodFeature = pd.concat([moodFeature, f])
            continue 
        
        if (moodFeature is None):
            moodFeature = calcMood(Id,f,affectData)
        else:
            moodFeature = pd.concat([moodFeature, calcMood(Id,f,affectData)])
        
        person_count += 1
        print 'Have processed %d people for mood feature' %person_count
        
    moodFeature.to_csv('moodFeature.csv', index=False)
    return moodFeature


def calcMood(Id,f,affectData):

    f['mood'] = 0.0

    for i in range((affectData.shape[0])/3):

        if (i == f.shape[0]):
            break

        j = i * 3
        todays_mood = affectData.iloc[j,2] + affectData.iloc[j+1,2] + affectData.iloc[j+2,2]

        f.iloc[i,4] = todays_mood

    return f

def energyOutcome():
    participantIDs = getDirNames('../CS120/')
    energyFeature = pd.DataFrame()
    person_count = 0
    
    for Id in participantIDs:
        
        f = labelEachDay(Id)
        f['day'] = np.arange(1,len(f)+1)
        f['id'] = Id;        
        
        affectFile = '../CS120/' + Id + '/emm.csv'
        if (os.path.isfile(affectFile)):
            affectData = csvToDataFrame(affectFile)
        else:
            f['energy'] = -1
            energyFeature = pd.concat([energyFeature, f])
            continue 
        
        if (energyFeature is None):
            energyFeature = calcEnergy(Id,f,affectData)
        else:
            energyFeature = pd.concat([energyFeature, calcEnergy(Id,f,affectData)])
        
        person_count += 1
        print 'Have processed %d people for energy feature' %person_count
        
    energyFeature.to_csv('energyFeature.csv', index=False)
    return energyFeature

def calcEnergy(Id,f,affectData):

    f['energy'] = 0.0

    for i in range((affectData.shape[0])/3):
        
        if (i == f.shape[0]):
            break

        j = i * 3
        todays_energy = affectData.iloc[j,3] + affectData.iloc[j+1,3] + affectData.iloc[j+2,3]

        f.iloc[i,4] = todays_energy

    return f

def focusOutcome():
    participantIDs = getDirNames('../CS120/')
    focusFeature = pd.DataFrame()
    person_count = 0
    
    for Id in participantIDs:
        
        f = labelEachDay(Id)
        f['day'] = np.arange(1,len(f)+1)
        f['id'] = Id;        
        
        affectFile = '../CS120/' + Id + '/emm.csv'
        if (os.path.isfile(affectFile)):
            affectData = csvToDataFrame(affectFile)
        else:
            f['focus'] = -1
            focusFeature = pd.concat([focusFeature, f])
            continue 
        
        if (focusFeature is None):
            focusFeature = calcFocus(Id,f,affectData)
        else:
            focusFeature = pd.concat([focusFeature, calcFocus(Id,f,affectData)])
        
        person_count += 1
        print 'Have processed %d people for focus feature' %person_count
        
    focusFeature.to_csv('focusFeature.csv', index=False)
    return focusFeature

def calcFocus(Id,f,affectData):

    f['focus'] = 0.0

    for i in range((affectData.shape[0])/3):

        if (i == f.shape[0]):
            break        

        j = i * 3
        todays_focus = affectData.iloc[j,4] + affectData.iloc[j+1,4] + affectData.iloc[j+2,4]

        f.iloc[i,4] = todays_focus

    return f


############################### run ######################################################
# complete datasets should have 10650 rows

#stress = stressOutcome()
#mood = moodOutcome()
#energy = energyOutcome()
#focus = focusOutcome()
#screen = screenStateFeatures()    
call = callStateFeatures()
sound = soundFeatures()
location = locationFeatures()      # ERROR
