from django.db.models import Sum
from utils_session import buildZonesList
from models import AllDayAllLoc, ByDaySepLoc, ByTimeAllLoc, PercentByTimeAllLoc
from models import Session, Location
from chartit import PivotChart, PivotDataPool
import datetime
import math

#
# utils_statistics 
# Contains methods used by views_admin.statistics to render statistical data in graph form based
# on the current Location and Session data.
# 
# Author: Chase Voorhees
# Email:  chase@cjvoorhees.com
#

#
# Generates a dict() containing chart0 and chart1, both JSON-string objects to be rendered by JQuery and Highcharts
#
def genCharts(date):
    
    # Gather data from Location, Session
    statDict = gather_stats(date)
    zoneDict = buildZonesList()


    # If the charts to be created are for ALL days
    if date == 'all':
    
        # Create chart: chtAllDayAllLoc - All days, all locations
        
        # Create AllDayAllLocObj's based on statDict
        for i in range(len(statDict['dateDict'])):        
            currentDate = statDict['dateDict'][i]
            #currentDateStr = currentDate.strftime('%a %m/%d')
            AllDayAllLocObj = AllDayAllLoc()
            AllDayAllLocObj.date = currentDate
            AllDayAllLocObj.numRegistered = statDict["numRegDict"][currentDate]
            AllDayAllLocObj.save()
        
        ds0 = PivotDataPool(
           series=
            [{'options': {
                'source': AllDayAllLoc.objects.all(),
                'categories': 'date'},
              'terms': {
                'Number_Registered':Sum('numRegistered')}}
             ]
        )
        
        chtAllDayAllLoc = PivotChart(
            datasource = ds0, 
            series_options = 
              [{'options':{
                  'type': 'column',
                  'stacking': False},
                'terms':['Number_Registered']}],
            chart_options = 
              {'title': {
                   'text': 'Number Registered, Grouped by Day for all Locations'},
               'xAxis': {
                    'title': {
                       'text': 'Date'}},
               'yAxis': {
                    'title': {
                       'text': 'Registrations'}}},
            )
        
        # Delete the objects we used to create the chart
        AllDayAllLocObjs = AllDayAllLoc.objects.all()
        for AllDayAllLocObj in AllDayAllLocObjs:
            AllDayAllLocObj.delete()
        
    
        
        # Create chart: chtByDaySepLoc - # Registered, separated by date and location
        
        # Create ByDaySepLocObj's based on statDict, zoneDict

        zoneDictStr = {}
        
        for x in range(10):
            building = zoneDict[x]['names']
            buildingStr = ""
            if building:
                for buildingName in building:
                    if buildingStr == "":
                        buildingStr = "Zone " + str(x) + " : " + buildingName
                    else:
                        buildingStr = buildingStr + ", " + buildingName   
            zoneDictStr[x] = buildingStr
            
        for i in range(len(statDict['dateDict'])):        
            currentDate = statDict['dateDict'][i]
            #currentDateStr = currentDate.strftime('%a %m/%d')
            
            for y in range(10):                
                ByDaySepLocObj = ByDaySepLoc()
                ByDaySepLocObj.numRegistered = statDict['numRegDictByZone'][currentDate].get(y, 0)
                ByDaySepLocObj.buildings = zoneDictStr[y]
                ByDaySepLocObj.date = currentDate
                if ByDaySepLocObj.buildings != "":
                    ByDaySepLocObj.save()
        
# See PivotDataPool API Ref: http://chartit.shutupandship.com/docs/apireference.html
# This was an attempt to change (shorten and add day of week) the x-axis labeling for the 'all' day charts.
# However, it broke the ordering - even with a custom sortf (sortf_mapf_mts(sortf, mapf, bool.map_then_sort))

#Add to series list: sortf_mapf_mts = (None, date_stringer, False)
#        def date_stringer(*t):
#            currentDate = datetime.datetime.strptime(t[0][0],'%Y-%m-%d')
#            dayStr = currentDate.strftime('%a')
#            monthStr = currentDate.strftime('%m')
#            dayNumStr = currentDate.strftime('%d')
#            if monthStr[0] == '0':
#                monthStr = monthStr[1:]
#            if dayStr[0] == '0':
#                dayStr = dayStr[1:]
#            monthDayStr = monthStr + "/" + dayNumStr
#            return (dayStr, monthDayStr)                
    
        ds1 = PivotDataPool(
      series= [
       {'options':{
          'source': ByDaySepLoc.objects.all(),
          'categories': ['date'],
          'legend_by': 'buildings'},
        'terms': {
          'num_registered':Sum('numRegistered')}}]
        )

        chtByDaySepLoc = PivotChart(
          datasource = ds1, 
          series_options = [
            {'options': {
               'type': 'column',
               'stacking': False, 
               'xAxis': 0,
               'yAxis': 0},
             'terms': ['num_registered']}],         
        chart_options = 
          {'title': {
               'text': 'Registrations by Day and Location'},
           'xAxis': {
                'title': {
                   'text': 'Date'}},
               'yAxis': {
                    'title': {
                       'text': 'Registrations'}}})
    
        # Delete the objects we used to create the chart
        ByDaySepLocObjs = ByDaySepLoc.objects.all()
        for ByDaySepLocObj in ByDaySepLocObjs:
            ByDaySepLocObj.delete()
    
    
        return {'chart0': chtAllDayAllLoc, 'chart1': chtByDaySepLoc}
    
    
    # If the charts to be created are for a SINGLE day
    else:
        # Create charts: chtByTimeAllLoc - # Registered, separated by time for a single date
        # and chtPercentByTimeAllLoc - % Registered, separated by time for a single date
        
        # Create ByTimeAllLocObj's AND PercentByTimeAllLocObj's based on statDict
        dateObj = datetime.datetime.strptime(date, '%Y-%m-%d')
        dateString = datetime.datetime.strftime(dateObj, '%A, %B %d, %Y')
        
        
        for i in range(len(statDict['hourDict'])):
            time = statDict['hourDict'][i]
            #date_and_time = datetime.datetime.combine(dateObj, time)
            #timeString = datetime.datetime.strftime(date_and_time, '%I:%M %p')
            # Pull the leading 0 off of the time if it's there (eg 08:40 AM)
            #if time.hour < 10:
            #    timeString = timeString[1:]

                      
            ByTimeAllLocObj = ByTimeAllLoc()
            ByTimeAllLocObj.date = dateString
            ByTimeAllLocObj.time = time
            ByTimeAllLocObj.numRegistered = statDict['numRegDict'][time]
            ByTimeAllLocObj.save()
            
            PercentByTimeAllLocObj = PercentByTimeAllLoc()
            PercentByTimeAllLocObj.date = dateString
            PercentByTimeAllLocObj.time = time
            PercentByTimeAllLocObj.percentRegistered = int(math.ceil(statDict['percentRegDict'][time]))
            PercentByTimeAllLocObj.save()
        
#        def time_stringer(*t):
#            currentTime = datetime.datetime.strptime(t[0][0],'%H:%M:%S')
#            hourStr = currentTime.strftime('%I')
#            if hourStr[0] == '0':
#                hourStr = hourStr[1:]
#            minStr = currentTime.strftime('%M')
#            return (hourStr, minStr)
        
        #sortf_mapf_mts = (None, time_stringer, False)
        
        ds0 = PivotDataPool(
           series=
            [{'options': {
                'source': ByTimeAllLoc.objects.all(),
                'categories': ['time']},
              'terms': {
                'Number Registered':Sum('numRegistered')}}
             ]         
        )
        
        chtByTimeAllLoc = PivotChart(
            datasource = ds0, 
            series_options = 
              [{'options':{
                  'type': 'column',
                  'stacking': False},
                'terms':['Number Registered']}],
            chart_options = 
              {'title': {
                   'text': 'Number Registered, Grouped by Time for ' + dateString},
               'xAxis': {
                    'title': {
                       'text': 'Time'}},
               'yAxis': {
                    'title': {
                       'text': 'Registrations'}}})
        
        # Delete the objects we used to create the chart
        ByTimeAllLocObjs = ByTimeAllLoc.objects.all()
        for ByTimeAllLocObj in ByTimeAllLocObjs:
            ByTimeAllLocObj.delete()
                 
#sortf_mapf_mts = (None, time_stringer, False)
        ds1 = PivotDataPool(
           series=
            [{'options': {
                'source': PercentByTimeAllLoc.objects.all(),
                'categories': ['time']},
              'terms': {
                'Percent Registered':Sum('percentRegistered')}}
             ])
        
        chtPercentByTimeAllLoc = PivotChart(
            datasource = ds1, 
            series_options = 
              [{'options':{
                  'type': 'column',
                  'stacking': False},
                'terms':['Percent Registered']}],
            chart_options = 
              {'title': {
                   'text': 'Percent Registered, Grouped by Time for ' + dateString},
               'xAxis': {
                    'title': {
                       'text': 'Time'}},
               'yAxis': {
                    'title': {
                       'text': 'Percent of Registration Capacity'}}})


        
        # Delete the objects we used to create the chart
        PercentByTimeAllLocObjs = PercentByTimeAllLoc.objects.all()
        for PercentByTimeAllLocObj in PercentByTimeAllLocObjs:
            PercentByTimeAllLocObj.delete()
    
        
        return {'chart0': chtByTimeAllLoc, 'chart1': chtPercentByTimeAllLoc}
        


#
# Generates a stats dictionary based on either date == 'all' or date = [specific date]
#
def gather_stats(date):
    
    if  date == 'all':
        currentSessions = Session.objects.all()
    
        # make a numRegDict[date] = # registered on that day     
        # and a numRegDictByZone[date][zone] = # reg on that day in that zone
        # and make a dictionary of the relevant dates dateDict[#] = date
        
        # compressed into one pass of currentSessions to avoid O(3N)
        
        numRegDict = dict()
        numRegDictByZone = dict()
        dateDict = dict()
        dateList = []

        for sessionInstance in currentSessions:
            if sessionInstance.date not in dateList:
                dateList.append(sessionInstance.date)        
            if numRegDict.get(sessionInstance.date, None) == None:
                numRegDict[sessionInstance.date] = sessionInstance.countID
                numRegDictByZone[sessionInstance.date] = dict()
                numRegDictByZone[sessionInstance.date][sessionInstance.zone] = sessionInstance.countID
            else:
                numRegDict[sessionInstance.date] = numRegDict[sessionInstance.date] + sessionInstance.countID
                if numRegDictByZone[sessionInstance.date].get(sessionInstance.zone, None) == None:
                    numRegDictByZone[sessionInstance.date][sessionInstance.zone] = sessionInstance.countID
                else:
                    numRegDictByZone[sessionInstance.date][sessionInstance.zone] = numRegDictByZone[sessionInstance.date][sessionInstance.zone] + sessionInstance.countID
    
        numDates = len(dateList)
        dateList.sort()
        dateList.reverse()
        for i in range(numDates):
            dateDict[i] = dateList.pop()
            
        #go thru zone #s 0-10, and add corresponding 
        #locations to currentZones dict()
        returnDictZones = dict()
        currentLocations = Location.objects.all()
        for i in range(11):
            returnDictZoneX = dict()
            returnListZoneX = []
            for locationInstance in currentLocations:
                if locationInstance.zoneNum == i:
                    returnListZoneX.append(locationInstance.name)
            
            returnListZoneX.sort()
            for x in range(len(returnListZoneX)):
                returnDictZoneX[x] = returnListZoneX[x]
            returnDictZones[i] = returnDictZoneX    
    
        # join all the dictionaries into a returnDict        
        returnDict = dict()
        returnDict['numRegDict'] = numRegDict
        returnDict['numRegDictByZone'] = numRegDictByZone
        returnDict['dateDict'] = dateDict
        returnDict['returnDictZones'] = returnDictZones
        
        return returnDict
    
    else:
        
        currentDate = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        
        # make the hour dictionary
        currentSessions = Session.objects.all()
        hourList = []
        hourDict = dict()
                
        # make the dict[hour] = # registered
        numRegDict = dict()
        
        # make the dict[hour] = max # registerable
        maxRegDict = dict()

        for sessionInstance in currentSessions:
            if sessionInstance.date == currentDate:
                if hourList.count(sessionInstance.time) > 0:
                    pass
                else:
                    hourList.append(sessionInstance.time)
                if numRegDict.get(sessionInstance.time, None) == None:
                    numRegDict[sessionInstance.time] = sessionInstance.countID
                else:
                    numRegDict[sessionInstance.time] = numRegDict[sessionInstance.time] + sessionInstance.countID
                if maxRegDict.get(sessionInstance.time, None) == None:
                    maxRegDict[sessionInstance.time] = sessionInstance.maxID
                else:
                    maxRegDict[sessionInstance.time] = maxRegDict[sessionInstance.time] + sessionInstance.maxID
                
        hourList.sort()
        for i in range(len(hourList)):
            hourDict[i] = hourList[i]            
        
        # make the percent reg'd dict[hour] = %
        percentRegDict = dict()
        for i in range(len(hourDict)):
            percentRegDict[hourDict[i]] = 100.0 * numRegDict[hourDict[i]] / maxRegDict[hourDict[i]]
        
        # combine the 3 dictionaries
        returnDict = dict()
        returnDict['hourDict'] = hourDict
        returnDict['numRegDict'] = numRegDict
        returnDict['percentRegDict'] = percentRegDict
        
        return returnDict

        