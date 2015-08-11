from models import Session, Location, WebsiteSettings
import datetime
from django.forms.models import model_to_dict

#
# hbs_parking session utils
# These utils are used to manipulate and call data from models.Location and models.Session
#
# Author: Chase Voorhees
# Email:  chase@cjvoorhees.com
# Author: Alex Kavanaugh
# Email : kavanaugh.development@outlook.com
#


#
# Load settings
#
def loadSettings():
    settings = WebsiteSettings.objects.get(id=1)
    returnDict = dict()
    returnDict['session_length'] = settings.session_length
    returnDict['status_is_open'] = settings.status_is_open
    returnDict['mode_is_move_in'] = settings.mode_is_move_in
    returnDict['term_code'] = settings.term_code
    return returnDict

#
# Creates session(s)
#
def makeSessions(date, startTime, endTime, minInterval, maxID, zone):
    # Convert string variables to usable objects
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    startTime = datetime.datetime.strptime(startTime, '%H:%M:%S').time()
    endTime = datetime.datetime.strptime(endTime, '%H:%M:%S').time()
    minInterval = int(minInterval)

    running = True
    while running:

        # Check to make sure startTime is before endTime
        currentTimeDelta = datetime.datetime.combine(datetime.date.today(), endTime) - datetime.datetime.combine(datetime.date.today(), startTime)

        if currentTimeDelta.total_seconds() < 0:
            running = False

        # Make the new session
        if running:
            currentSession = Session()
            currentSession.date = date
            currentSession.maxID = int(maxID)
            currentSession.zone = int(zone)
            currentSession.countID = 0
            currentSession.time = startTime
            currentSession.save()

            # Increment startTime by minInterval        
            startTime = (datetime.datetime.combine(datetime.date.today(), startTime) + datetime.timedelta(minutes=minInterval)).time()

#
# Build current zones dictionary
#
def buildZonesList():
    currentLocations = Location.objects.all()
    zones = dict()
    for i in range(11):
        location_list = []
        for locationInstance in currentLocations:
            if locationInstance.zoneNum == i:
                location_list.append(locationInstance.name)
        zones[i] = dict()
        zones[i]['number'] = i
        zones[i]['names'] = location_list
    return zones

#
# Build a dictionary of sessions, sorted by date and then time
# returnDict[0][0], for instance, is a session during the first time slot of the first day
#
def buildSessionsList():
    # Build list of current sessions
    currentSessions = list(Session.objects.all())
    currentSessions.sort(key=lambda x: x.date)

    currentDate = None
    numDates = 0
    dayList = []
    returnDict = dict()

    for i in range(len(currentSessions)):
        # First pass, set current date
        if currentDate is None:
            currentDate = currentSessions[i].date
        # Date is the same, add object to dayList
        if currentDate == currentSessions[i].date:
            dayList.append(currentSessions[i])
        # Date has changed, dump and render current dayList and create a new one
        else:
            # Set new current date
            currentDate = currentSessions[i].date

            # Sort the dayList by time slot
            dayList.sort(key=lambda x: x.time)
            dayDict = dict()

            # Create time sorted dictionary
            for x in range(len(dayList)):
                dayDict[x] = model_to_dict(dayList[x], fields=[field.name for field in dayList[x]._meta.fields])

            # Add to day sorted dictionary
            returnDict[numDates] = dayDict
            numDates = numDates + 1

            # Create new dayList and add current day to it
            dayList = []
            dayList.append(currentSessions[i])

        # If this is the last iteration, dump and render new dayList
        if i == len(currentSessions) - 1:
            # Sort the dayList by time slot
            dayList.sort(key=lambda x: x.time)
            dayDict = dict()

            # Create time sorted dictionary
            for x in range(len(dayList)):
                dayDict[x] = model_to_dict(dayList[x], fields=[field.name for field in dayList[x]._meta.fields])

            # Add to day sorted dictionary
            returnDict[numDates] = dayDict
    return returnDict

def home_check_session_placement(session, community):
    # Build current zones dictionary
    zones = buildZonesList()

    if community == 'PCV':
        for name in zones[session.zone]['names']:
            if name == 'Bishop' or name == 'Cabrillo' or name == 'Islay' or name == 'Morro' or name == 'Romauldo' or name == 'Cerro Vista (All)' or name == 'Cerro Vista (FR/TR)' or name == 'Hollister' or name == 'Cerro San Luis':
                return False
        return True

    elif community == 'CV':
        for name in zones[session.zone]['names']:
            if name == 'Aliso' or name == 'Buena Vista' or name == 'Corralitos' or name == 'Dover' or name == 'Estrella' or name == 'Foxen' or name == 'Gypsum' or name == 'Huasna' or name == 'Inyo' or name == 'Poly Canyon Village (All)' or name == 'Poly Canyon Village (FR/TR)':
                return False
        return True
    else:
        return False


def home_build_dict(currentSessions):
    currentSessions.sort(key=lambda x: x.date)

    currentDate = None
    numDates = 0
    dayList = []
    returnDict = dict()

    # Check if there is any data to sort
    if len(currentSessions) == 0:
        return returnDict

    for i in range(len(currentSessions)):
        # First pass, set current date
        if currentDate is None:
            currentDate = currentSessions[i].date
        # Date is the same, add object to dayList
        if currentDate == currentSessions[i].date:
            dayList.append(currentSessions[i])
        # Date has changed, dump and render current dayList and create a new one
        else:
            # Set new current date
            currentDate = currentSessions[i].date

            # Sort the dayList by time slot
            dayList.sort(key=lambda x: x.time)

            # Add to day sorted dictionary
            returnDict[numDates] = dict()
            returnDict[numDates]['date'] = dayList[0].date
            returnDict[numDates]['start_time'] = dayList[0].time
            returnDict[numDates]['end_time'] = dayList[len(dayList) - 1].time
            numDates = numDates + 1

            # Create new dayList and add current day to it
            dayList = []
            dayList.append(currentSessions[i])

        # If this is the last iteration, dump and render new dayList
        if i == len(currentSessions) - 1:
            # Sort the dayList by time slot
            dayList.sort(key=lambda x: x.time)

            # Add to day sorted dictionary
            returnDict[numDates] = dict()
            returnDict[numDates]['date'] = dayList[0].date
            returnDict[numDates]['start_time'] = dayList[0].time
            returnDict[numDates]['end_time'] = dayList[len(dayList) - 1].time

    return returnDict
