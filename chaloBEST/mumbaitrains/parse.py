from pyquery import PyQuery as pq
from models import *
import datetime

BASE_URL = 'http://mumbailifeline.com/'

'''
eg.:
>>>parseURL('http://mumbailifeline.com/timetable.php?sel_route=central&sfrom=Mumbai_CST&sto=Masjid&time1=4:00%20am&time2=11:59%20PM', Central')
'''
def parseURL(url, line):
    d = pq(url=url)
    table = d('#gradient-style')
    trs = table.find('tr')
    for i in range(1,len(trs)):
        thisTr = trs[i]
        td = thisTr.getchildren()[0]
        a = td.find('a')
        trainNo = a.text.strip()
        print "Saving %s ... " % trainNo
        trainURL = BASE_URL + a.get('href').strip()
        saveTrain(trainURL, trainNo, line)


def saveTrain(url, no, line):
    train, created = Train.objects.get_or_create(number=no, line=line)
    if not created:
        print "Train no %s already exists in db, skipping" % no
        return
    train.save()
    d = pq(url=url)
    table = d.find('table')[3]
    for tr in table.iterfind('tr'):
        children = tr.getchildren()
        serial = 0
        if len(tr.findall('td')) > 0:
            td0 = children[0]
            a = td0.find('a')
            stationName = a.text.strip()
            station, created = Station.objects.get_or_create(name=stationName)
            timeString = children[1].find('strong').text
            hour = int(timeString.split(":")[0].strip()) - 1
            mins = int(timeString.split(":")[1][0:2])
            ampm = timeString[-2:]
            if ampm == 'pm':
                hour = hour + 12
            stationTime = datetime.time(hour,mins)
            st = TrainStation(train=train, station=station, time=stationTime, serial=serial)
            st.save()
            serial += 1
    print "Saved %s" % no                 

