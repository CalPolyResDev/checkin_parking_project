from hbs_parking.rmsConnector.utils import get_rmsID
from django.core.urlresolvers import reverse
from models import Session, Location, WebsiteSettings
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from hbs_parking.main.utils_session import loadSettings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

#
# hbs_parking ajax methods
#
# Author: Alex Kavanaugh
# Email:  kavanaugh.development@outlook.com
#

@dajaxice_register
def request_deleteSessions(request, sessionIDList, totalBoxes, table_id):
    dajax = Dajax()
    sessionList_clean = []

    # Clean session list
    for sessionID in sessionIDList:
        sessionID_clean = sessionID.split('session_')[1]
        currentSession = Session.objects.filter(id=sessionID_clean)[0]

        # Return an error if one of the sessions cannot be deleted
        if currentSession.countID > 0:
            dajax.alert("One or more sessions could not be deleted. A session cannot be deleted if residents have already registered for it.")
            return dajax.json()

        sessionList_clean.append(currentSession)

    # Delete sessions in sessionList from database
    for session in sessionList_clean:
        session.delete()

    # Delete sessions in sessionList from html table,
    # Remove the whole table if there are no rows left
    sessionList_length = totalBoxes - len(sessionIDList)
    if sessionList_length < 1:
        dajax.remove('#date_div_' + str(table_id))
    else:
        for session in sessionIDList:
            dajax.remove('#' + session + "_tr")
            sessionList_length = sessionList_length - 1
    dajax.assign('#checkboxButton_' + str(table_id), "disabled", True)

    return dajax.json()

@dajaxice_register
def request_modifyZone(request, locationList, zoneKey):
    dajax = Dajax()

    # Clean the zoneKey
    zoneKey_clean = zoneKey.split('sortable_zone_')[1]
    if zoneKey_clean == 'null':
        zoneKey_clean = None
    else:
        zoneKey_clean = int(zoneKey_clean)

    # Change the zone numbers for each location in the list
    for locationKey in locationList:
        LocationInstance = Location.objects.filter(key=locationKey)[0]
        LocationInstance.zoneNum = zoneKey_clean
        LocationInstance.save()

    return dajax.json()

@dajaxice_register
def request_reserveSession(request, sessionID):
    dajax = Dajax()
    userID = request.user.username
    try:
        rmsID = get_rmsID(userID)
    except ObjectDoesNotExist:
        dajax.alert("You cannot reserve a session as an administrator.")
        return dajax.json()
    if sessionID != None:
        # Modify Session data
        regSession = Session.objects.get(id=sessionID)

        if regSession.countID >= regSession.maxID:
            dajax.alert("This session has already been filled.")
            return dajax.json()

        # Make sure the ID isn't already in the rmsID string
        if regSession.rmsID.split(",").count(str(rmsID)) > 0:
            dajax.alert("You are already registered for this session.")
            return dajax.json()

        regSession.countID = regSession.countID + 1
        if regSession.rmsID == "":
            regSession.rmsID = str(rmsID)
        else:
            regSession.rmsID = regSession.rmsID + "," + str(rmsID)
        regSession.save()

        # Change user's reservation status
        user = get_user_model
        user.has_reserved = True
        user.save()

    dajax.redirect(reverse('view-reservation'))
    return dajax.json()

@dajaxice_register
def request_changeReservation(request, sessionID=None):
    dajax = Dajax()
    userID = request.user.username
    try:
        rmsID = get_rmsID(userID)
    except ObjectDoesNotExist:
        dajax.alert("You cannot reserve a session as an administrator.")
        return dajax.json()
    if sessionID != None:
        # Modify Session data
        regSession = Session.objects.get(id=sessionID)

        if regSession.countID > 0:
            regSession.countID = regSession.countID - 1

        idList = regSession.rmsID.split(",")
        idList.remove(str(rmsID))

        rmsIDStr = ""

        for rmsIDInst in idList:
            if rmsIDStr == "":
                rmsIDStr = rmsIDInst
            else:
                rmsIDStr = rmsIDStr + "," + rmsIDInst

        regSession.rmsID = rmsIDStr
        regSession.save()

        # Change user's reservation status
        user = get_user_model
        user.has_reserved = True
        user.save()


    dajax.redirect(reverse('reserve-session'))
    return dajax.json()

@dajaxice_register
def request_controlPanel(request, switch, toggle):
    # Update database
    settings = WebsiteSettings.objects.get(id=1)
    if switch == 'rStatus':
        if toggle == 'on':
            settings.status_is_open = True
        else:
            settings.status_is_open = False
    elif switch == 'wMode':
        if toggle == 'on':
            settings.mode_is_move_in = True
        else:
            settings.mode_is_move_in = False
    settings.save()

    # Update session variables
    request.session['settings'] = loadSettings()

    dajax = Dajax()
    dajax.redirect(reverse('control-panel'))
    return dajax.json()

@dajaxice_register
def request_purgeTables(request):
    # Purge users
    currentUsers = User.objects.all()
    for userInstance in currentUsers:
        if not userInstance.is_staff and not userInstance.is_developer:
            userInstance.delete()
    # Truncate sessions
    Session.objects.all().delete()

    dajax = Dajax()
    dajax.redirect(reverse('control-panel'))
    return dajax.json()

@dajaxice_register
def request_purgeRegs(request):
    # Purge users
    currentUsers = User.objects.all()
    for userInstance in currentUsers:
        if not userInstance.is_staff and not userInstance.is_developer:
            userInstance.delete()
    # Cut Registrations from sessions
    currentSessions = Session.objects.all()
    for sessionInstance in currentSessions:
        sessionInstance.countID = 0
        sessionInstance.rmsID = ""
        sessionInstance.save()

    dajax = Dajax()
    dajax.redirect(reverse('control-panel'))
    return dajax.json()
