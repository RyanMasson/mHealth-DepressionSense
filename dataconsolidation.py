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
    if not os.path.exists(path_to_file):
        return None
    data = open(path_to_file).readlines()
    for row in data:
        row = [x.rstrip() for x in row.split('\t')]
        if row != ['']:
            csvData.append(row)
    return pd.DataFrame(csvData)

def getDirNames(path_to_directory):
    names = os.listdir(path_to_directory)
    names.pop(0)
    badfile = names.index("desktop.ini")
    del names[badfile]
    return names

def getFileNames(path_to_directory):
    names = [f for f in listdir(path_to_directory) if isfile(join(path_to_directory, f)) and 'DS_Store' not in f and 'Sohrob' not in f]
    return names

#inputs are strings
def isSameDay(timestamp1, timestamp2):
    if '"' in timestamp1:
        timestamp1 = timestamp1.replace('"','')
    if '"' in timestamp2:
        timestamp2 = timestamp2.replace('"', '')
    date1 = datetime.utcfromtimestamp(float(timestamp1)).strftime('%Y-%m-%d')
    date2 = datetime.utcfromtimestamp(float(timestamp2)).strftime('%Y-%m-%d')
    return date1 == date2

#inputs are strings
def isEarlier(sensor_ts,day_ts):
    if '"' in sensor_ts:
        sensor_ts = sensor_ts.replace('"','')
    if '"' in day_ts:
        day_ts = day_ts.replace('"', '')
    return float(sensor_ts) < float(day_ts)

def labelEachDay(participantID):
    sleepFile = '../CS120/' + participantID + '/ems.csv'
    sleepReport = csvToDataFrame(sleepFile)
    if sleepReport is None:
        return None
    sleepReport = sleepReport.drop(sleepReport.columns[1:6], axis=1)
    sleepReport.columns = ['timestamp','label']
    sleepReport['day'] = np.arange(1, len(sleepReport) + 1)
    sleepReport['id'] = participantID;
    return sleepReport

def addAdditionalWifi(path):
    participantIDs, df = createLabelDF(path)
    days = len(df)

    points = [[] for _ in range(days)]

    featureNames = ['wifi_max', 'wifi_min', 'wifi_std']

    maxwifi = np.full((days, 1), -1)
    minwifi = np.full((days, 1), -1)
    stdwifi = np.full((days, 1), -1)

    for id in participantIDs:
        wifiFile = '../CS120/' + id + '/wif.csv'
        wifiReport = csvToDataFrame(wifiFile)
        relevant_rows = df.loc[df['id'] == id]

        if wifiReport is not None:
            index = 0
            i = 0
            start = relevant_rows.index[0]

            while index < len(relevant_rows.index):
                row_i = index + start
                row = df.iloc[[row_i]]

                day_ts = row['timestamp'][row_i]

                while i < len(wifiReport):
                    ts = wifiReport[0][i]
                    accessPoints = wifiReport[3][i]
                    if '"' in accessPoints:
                        accessPoints = accessPoints.replace('"', '')
                    accessPoints = float(accessPoints)

                    if isSameDay(ts,day_ts):
                        arr = points[row_i].append(accessPoints)
                        i += 1
                    elif isEarlier(ts, day_ts):
                        i += 1
                    else:
                        break
                index += 1
                a = points[row_i]
                if a:
                    maxwifi[row_i][0] = np.max(a)
                    minwifi[row_i][0] = np.min(a)
                    stdwifi[row_i][0] = np.std(a)

    return featureNames, [maxwifi, minwifi, stdwifi]

def addLight(path):
    participantIDs, df = createLabelDF(path)
    featureNames = ['lgt_mean', 'lgt_std']

    days = len(df)

    avg_intensities = [[] for _ in range(days)]

    avg_intensity_mean = np.full((days, 1), -1)
    avg_intensity_std = np.full((days, 1), -1)

    for id in participantIDs:
        print id
        lgtFile = '../CS120/' + id + '/lgt.csv'
        lgtReport = csvToDataFrame(lgtFile)
        relevant_rows = df.loc[df['id'] == id]

        if lgtReport is not None:
            index = 0
            i = 0
            start = relevant_rows.index[0]

            while index < len(relevant_rows.index):
                row_i = index + start
                row = df.iloc[[row_i]]

                day_ts = row['timestamp'][row_i]

                while i < len(lgtReport):
                    ts = lgtReport[0][i]
                    intensity = float(lgtReport[1][i])
                    accuracy = lgtReport[2][i]
                    if '"' in accuracy:
                        accuracy = accuracy.replace('"', '')
                    accuracy = float(accuracy)

                    if accuracy == 0:
                        i += 1
                    elif isSameDay(ts, day_ts):
                        arr = avg_intensities[row_i]
                        arr.append(intensity)
                        i += 1
                    else:
                        break
                index += 1
                a = avg_intensities[row_i]
                if a:
                    avg_intensity_mean[row_i][0] = np.mean(a)
                    avg_intensity_std[row_i][0] = np.std(a)

    return featureNames, [avg_intensity_mean, avg_intensity_std]

def addBattery(path):
    participantIDs, df = createLabelDF(path)
    featureNames = ['min_batt_level','total_pluggedin_time','charger_perc','usb_perc','freq_plugged','freq_unplugged']

    days = len(df)

    min_bat_level = np.full((days, 1), -1)
    pluggedin_time = np.full((days, 1), -1)

    charger_perc = np.full((days, 1), -1)
    usb_perc = np.full((days, 1), -1)

    freq_plugged = np.full((days, 1), -1)
    freq_unplugged = np.full((days, 1), -1)


    for id in participantIDs:
        battFile = '../CS120/' + id + '/bat.csv'
        battReport = csvToDataFrame(battFile)
        relevant_rows = df.loc[df['id'] == id]

        print "participant ", id

        if battReport is not None:
            start = relevant_rows.index[0]
            end = relevant_rows.shape[0]
            index = 0
            i = 0

            while index < len(relevant_rows.index):
                row_i = index + start
                row = df.iloc[[row_i]]
                day_ts = row['timestamp'][row_i]
                plugged_prev = 0
                ts_prev = -1

                freq_unplugged_day = 0
                freq_plugged_day = 0
                min = -1
                pluggedin_time_day = 0
                charger_day = 0
                usb_day = 0

                while i < len(battReport):

                    ts = battReport[0][i]

                    if '"' in ts:
                        ts = ts.replace('"', '')
                    batt_level = float(battReport[1][i])
                    batt_plugged = battReport[2][i]

                    if '"' in batt_plugged:
                        batt_plugged = batt_plugged.replace('"', '')
                    batt_plugged = int(batt_plugged) # 0 = unplugged, 1 = charger, 2 = usb

                    if isSameDay(ts, day_ts):
                        if plugged_prev == 0 and batt_plugged > 0:    # 0 change to 1 or 2
                            freq_unplugged_day += 1
                        elif batt_plugged == 0 and plugged_prev > 0:     # 1 or 2 change to 0
                            freq_plugged_day += 1
                            pluggedin_time_day += float(ts) - ts_prev

                            if plugged_prev == 1:
                                charger_day += 1
                            elif plugged_prev == 2:
                                usb_day += 1

                        elif batt_plugged > 0 and plugged_prev > 0:     # 1 or 2 change to 1 or 2
                            pluggedin_time_day += float(ts) - ts_prev
                            if batt_plugged == 1 and plugged_prev == 2:
                                usb_day += 1
                                freq_plugged_day += 1
                            elif batt_plugged == 2 and plugged_prev == 1:
                                charger_day += 1
                                freq_plugged_day += 1

                        plugged_prev = batt_plugged
                        ts_prev = float(ts)

                        if min < 0:
                            min = batt_level
                        elif min > batt_level:
                            min = batt_level

                        i += 1
                    else:
                        break

                pluggedin_time[row_i][0] = pluggedin_time_day
                min_bat_level[row_i][0] = min
                freq_plugged[row_i][0] = freq_plugged_day
                freq_unplugged[row_i][0] = freq_unplugged_day
                total = charger_day + usb_day
                charger_perc[row_i][0] = charger_day / total if total > 0 else 0
                usb_perc[row_i][0] = usb_day / total if total > 0 else 0

                index += 1

    return featureNames, [min_bat_level, pluggedin_time, charger_perc, usb_perc, freq_plugged,freq_unplugged]


def addComunication(path):
    participantIDs, df = createLabelDF(path)

    days = len(df)

    # Communication type
    sms = np.full((days, 1), -1)
    call = np.full((days, 1), -1)

    # Communication direction
    missed = np.full((days, 1), -1)
    outgoing = np.full((days, 1), -1)
    incoming = np.full((days, 1), -1)

    featureNames = ['sms_perc', 'call_perc', 'missed_perc', 'outgoing_perc', 'incoming_perc','freq_sms','freq_calls','freq_outgoing','freq_incoming','freq_missed']
    sms_perc = np.full((days, 1), -1)
    call_perc = np.full((days, 1), -1)
    missed_perc = np.full((days, 1), -1)
    outgoing_perc = np.full((days, 1), -1)
    incoming_perc = np.full((days, 1), -1)

    for id in participantIDs:
        commFile = '../CS120/' + id + '/coe.csv'
        commReport = csvToDataFrame(commFile)
        relevant_rows = df.loc[df['id'] == id]

        if commReport is not None and not relevant_rows.empty:
            index = 0
            start = relevant_rows.index[0]
            for i in range(len(commReport)):
                ts = commReport[0][i]
                comm_type = commReport[3][i]
                comm_dir = commReport[4][i]
                if comm_dir == None:
                    break

                comm_dir = comm_dir.replace('"', '')

                while (index < len(relevant_rows.index)):
                    row_i = index + start
                    row = df.iloc[[row_i]]

                    if (row['id'][row_i] != id):
                        index += 1
                        break
                    day_ts = row['timestamp'][row_i]
                    if isSameDay(ts, day_ts):
                        if comm_type == 'SMS':
                            if sms[row_i][0] == -1:
                                sms[row_i][0] = 1
                            else:
                                sms[row_i][0] += 1
                        elif comm_type == 'PHONE':
                            if call[row_i][0] == -1:
                                call[row_i][0] = 1
                            else:
                                call[row_i][0] += 1
                        if comm_dir == 'MISSED':
                            if missed[row_i][0] == -1:
                                missed[row_i][0] = 1
                            else:
                                missed[row_i][0] += 1
                        elif comm_dir == 'OUTGOING':
                            if outgoing[row_i][0] == -1:
                                outgoing[row_i][0] = 1
                            else:
                                outgoing[row_i][0] += 1
                        elif comm_dir == 'INCOMING':
                            if incoming[row_i][0] == -1:
                                incoming[row_i][0] = 1
                            else:
                                incoming[row_i][0] += 1
                        break
                    elif isEarlier(ts, day_ts):
                        break

                    index += 1

            for i in range(days):
                s = sms[i][0]
                c = call[i][0]
                sc = s+c

                m = missed[i][0]
                o = outgoing[i][0]
                inc = incoming[i][0]
                moi = m+o+inc

                sms_perc[i][0]= s / sc if sc > 0 else -1
                call_perc[i][0] = c / sc if sc > 0 else -1
                missed_perc[i][0] = m / moi if moi > 0 else -1
                outgoing_perc[i][0] = o / moi if moi > 0 else -1
                incoming_perc[i][0] = inc / moi if moi > 0 else -1

    return featureNames, [sms_perc, call_perc, missed_perc, outgoing_perc, incoming_perc,sms,call,outgoing,incoming,missed]


def addAdditionalCommunication(path):
    participantIDs, df = createLabelDF(path)

    days = len(df)

    # Communication type
    uniqueCommunication = np.full((days, 1), -1)

    people = [[] for _ in range(days)]

    featureNames = ['people_communication_num']

    for id in participantIDs:

        commFile = '../CS120/' + id + '/coe.csv'
        commReport = csvToDataFrame(commFile)
        relevant_rows = df.loc[df['id'] == id]

        if commReport is not None and not relevant_rows.empty:
            index = 0
            start = relevant_rows.index[0]
            i = 0

            while index < len(relevant_rows.index):
                row_i = index + start
                row = df.iloc[[row_i]]
                day_ts = row['timestamp'][row_i]

                while i < len(commReport):
                    ts = commReport[0][i]
                    person = commReport[1][i]

                    if isSameDay(ts, day_ts):
                        people[row_i].append(person)
                        i += 1
                    elif isEarlier(ts, day_ts):
                        i += 1
                    else:
                        break

                index += 1

                uniqueCommunication[row_i][0] = len(set(people[row_i]))

    return featureNames, [uniqueCommunication]

def createBigCSV(path_to_directory):
    participantIDs = getDirNames(path_to_directory)

    for Id in participantIDs:
        labels = labelEachDay(Id)
        if labels is not None:

            addWifiMean(Id,labels)

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

def createLabelDF(path):
    participantIDs = getDirNames(path)
    labels = None
    for Id in participantIDs:
        if labels is None:
            labels = labelEachDay(Id)
        else:
            labels = labels.append(labelEachDay(Id),ignore_index=True)
    return participantIDs,labels

def addSound(path):
    participantIDs, df = createLabelDF(path)
    featureNames = ['normPower_mean', 'normPower_max','normPower_min','normPower_var','dominantFreq_mean','dominantFreq_max','dominantFreq_min','dominantFreq_var', 'normAmp_mean','normAmp_var']

    days = len(df)

    normPower= [[] for _ in range(days)]
    domFreq = [[] for _ in range(days)]
    normAmp = [[] for _ in range(days)]

    normPower_mean = np.full((days, 1), -1)
    normPower_max = np.full((days, 1), -1)
    normPower_min = np.full((days, 1), -1)
    normPower_var = np.full((days, 1), -1)

    dominantFreq_mean = np.full((days, 1), -1)
    dominantFreq_max = np.full((days, 1), -1)
    dominantFreq_min = np.full((days, 1), -1)
    dominantFreq_var = np.full((days, 1), -1)

    normAmp_mean = np.full((days, 1), -1)
    normAmp_var = np.full((days, 1), -1)

    for id in participantIDs:

        audFile = '../CS120/' + '25349' + '/aud.csv'
        audReport = csvToDataFrame(audFile)
        relevant_rows = df.loc[df['id'] == '25349']

        if audReport is not None:
            index = 0
            i = 0
            start = relevant_rows.index[0]

            while index < len(relevant_rows.index):
                row_i = index + start
                row = df.iloc[[row_i]]

                day_ts = row['timestamp'][row_i]

                while i < len(audReport):
                    ts = audReport[0][i]

                    power = audReport[1][i]
                    freq = audReport[2][i]
                    mag = audReport[3][i]

                    if '"' in power:
                        power = power.replace('"', '')
                    power = float(power)
                    if '"' in freq:
                        freq = freq.replace('"', '')
                    freq = float(freq)
                    if '"' in mag:
                        mag = mag.replace('"', '')
                    mag = float(mag)

                    if isSameDay(ts,day_ts):
                        normPower[row_i].append(power)
                        domFreq[row_i].append(freq)
                        normAmp[row_i].append(mag)
                        i += 1
                    elif isEarlier(ts, day_ts):
                        i += 1
                    else:
                        break
                index += 1
                a = normPower[row_i]
                if a:
                    normPower_mean[row_i][0] = np.mean(a)
                    aa = np.mean(a)
                    normPower_max[row_i][0] = np.max(a)
                    ab = np.max(a)
                    normPower_min[row_i][0] = np.min(a)
                    ac = np.min(a)
                    normPower_var[row_i][0] = np.var(a)
                    ad = np.var(a)
                b = domFreq[row_i]
                if b:
                    dominantFreq_mean[row_i][0] =np.mean(b)
                    ae = np.mean(b)
                    dominantFreq_max[row_i][0] =np.max(b)
                    af = np.max(b)
                    dominantFreq_min[row_i][0] = np.min(b)
                    ag = np.min(b)
                    dominantFreq_var[row_i][0] =np.var(b)
                    ah = np.var(b)
                c = normAmp[row_i]
                if c:
                    normAmp_mean[row_i][0] =np.mean(c)
                    ai = np.mean(c)
                    aj = np.var(c)
                    normAmp_var[row_i][0] =np.var(c)
    return featureNames, [normPower_mean, normPower_max, normPower_min, normPower_var,
                                dominantFreq_mean, dominantFreq_max, dominantFreq_min, dominantFreq_var,
                                normAmp_mean, normAmp_var]

def addCallstate(path):
    participantIDs, df = createLabelDF(path)
    featureNames = ['idle_perc','ringing_perc','offhook_perc']

    days = len(df)

    idle = [0] * days
    ringing = [0] * days
    offhook = [0] * days

    idle_perc = np.full((days, 1), -1)
    ringing_perc = np.full((days, 1), -1)
    offhook_perc = np.full((days, 1), -1)

    for id in participantIDs:

        audFile = '../CS120/' + id + '/cal.csv'
        audReport = csvToDataFrame(audFile)
        relevant_rows = df.loc[df['id'] == id]

        if audReport is not None:
            index = 0
            i = 0
            start = relevant_rows.index[0]

            while index < len(relevant_rows.index):
                row_i = index + start
                row = df.iloc[[row_i]]

                day_ts = row['timestamp'][row_i]

                while i < len(audReport):
                    ts = audReport[0][i]

                    callstate = audReport[1][i]

                    if '"' in callstate:
                        callstate = callstate.replace('"', '')

                    if isSameDay(ts, day_ts):
                        if callstate == 'Idle':
                            idle[row_i] += 1
                        elif callstate == 'Ringing':
                            ringing[row_i] += 1
                        elif callstate == 'Off-Hook':
                            offhook[row_i] += 1
                        i += 1
                    elif isEarlier(ts, day_ts):
                        i += 1
                    else:
                        break
                index += 1
                i = idle[row_i]
                r = ringing[row_i]
                o = offhook[row_i]
                total = i + r + o
                idle_perc[row_i][0] = i / total if total > 0 else -1
                ringing_perc[row_i][0] = r / total if total > 0 else -1
                offhook_perc[row_i][0] = o / total if total > 0 else -1

    return featureNames, [idle_perc,ringing_perc,offhook_perc]

############ RUN ####################
path_to_CS120 = ''
createBigCSV(path_to_CS120)  # create initial csv file with timestamp,day,id,label and wifimean

# Add rest of wifi features
additionalWifiNames, additionalWifiFeatures = addAdditionalWifi(path_to_CS120)
for i in range(len(additionalWifiNames)):
    addFeature2csv(additionalWifiNames[i],additionalWifiFeatures[i])

# Add light features
lightNames, lightFeatures = addLight(path_to_CS120)
for i in range(len(lightNames)):
    addFeature2csv(lightNames[i],lightFeatures[i])

# Add battery features
batteryNames, batteryFeatures = addBattery(path_to_CS120)
for i in range(len(batteryNames)):
    addFeature2csv(batteryNames[i],batteryFeatures[i])

# Add communication features
communicationNames, communicationFeatures = addComunication(path_to_CS120)
for i in range(len(communicationNames)):
    addFeature2csv(communicationNames[i],communicationFeatures[i])
communicationAdditionalNames, communicationAdditionalFeatures = addAdditionalCommunication(path_to_CS120)
for i in range(len(communicationAdditionalNames)):
    addFeature2csv(communicationAdditionalNames[i],communicationAdditionalFeatures[i])

# Add sound features
soundNames, soundFeatures = addSound(path_to_CS120)
for i in range(len(soundNames)):
    addFeature2csv(soundNames[i],soundFeatures[i])

# Add call features
callNames, callFeatures = addCallstate(path_to_CS120)
for i in range(len(callNames)):
    addFeature2csv(callNames[i],callFeatures[i])

