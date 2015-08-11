from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotFound
from django.forms.models import model_to_dict
from utils_session import makeSessions, buildZonesList, buildSessionsList
from django.contrib.auth.decorators import user_passes_test
from utils_statistics import genCharts
from hbs_parking.rmsConnector.utils import get_rmsID, get_alias
from forms import SessionForm, addSessionForm, aliasSearchForm, RMSSearchForm, ZoneTextForm, TermCodeForm, PDFMapForm
from models import Session, Location, Zone, WebsiteSettings
from django.forms.util import ErrorList
from django.forms.forms import NON_FIELD_ERRORS
from django.core.urlresolvers import reverse
from django.conf import settings
import os, datetime, time

#
# Lists session data
#
@user_passes_test(admin_test)
def listSessions(request):
    template_name = "main/admin/listSessions.html"

    # Build current zones dictionary
    returnDictZones = buildZonesList()

    # Build current sessions dictionary
    returnDictSessions = buildSessionsList()

    return render_to_response(template_name, {'data': returnDictSessions, 'zones': returnDictZones}, context_instance=RequestContext(request))

#
# Presents the user with a form to add session data
#
@user_passes_test(admin_test)
def addSession(request):
    template_name = "main/admin/addSession.html"
    returnDict = dict()

    # Build current zones dictionary
    returnDict['zones'] = buildZonesList()

    # User submitted an add session request
    if request.method == 'POST':
        form = addSessionForm(data=request.POST)

        if form.is_valid():
            errors = form._errors.setdefault(NON_FIELD_ERRORS, ErrorList())

            for i in range(5):
                if request.POST['zone' + str(i)] != "":
                    startTime = request.POST['start_time']
                    endTime = request.POST['end_time']
                    minInterval = request.POST['interval']
                    maxID = request.POST['capacity']
                    zone = request.POST['zone' + str(i)]

                    try:
                        date = request.POST['date0']
                        makeSessions(date, startTime, endTime, minInterval, maxID, zone)
                    except (RuntimeError, TypeError, NameError):
                        errors.append(u'Date 1 could not be parsed.')
                    if request.POST['date1'] != "":
                        try:
                            date = request.POST['date1']
                            makeSessions(date, startTime, endTime, minInterval, maxID, zone)
                        except (RuntimeError, TypeError, NameError):
                            errors.append(u'Date 2 could not be parsed.')
                    if request.POST['date2'] != "":
                        try:
                            date = request.POST['date2']
                            makeSessions(date, startTime, endTime, minInterval, maxID, zone)
                        except (RuntimeError, TypeError, NameError):
                            errors.append(u'Date 3 could not be parsed.')
                    if request.POST['date3'] != "":
                        try:
                            date = request.POST['date3']
                            makeSessions(date, startTime, endTime, minInterval, maxID, zone)
                        except (RuntimeError, TypeError, NameError):
                            errors.append(u'Date 4 could not be parsed.')
                    if request.POST['date4'] != "":
                        try:
                            date = request.POST['date4']
                            makeSessions(date, startTime, endTime, minInterval, maxID, zone)
                        except (RuntimeError, TypeError, NameError):
                            errors.append(u'Date 5 could not be parsed.')

                    if len(errors):
                        return render_to_response(template_name, {'form': form, 'data': returnDict}, context_instance=RequestContext(request))

            # Redirect to the session list
            return HttpResponseRedirect(reverse('list-sessions'))

    # User is viewing the add session page
    else:
        form = addSessionForm()

    request.session.set_test_cookie()

    return render_to_response(template_name, {'form': form, 'data': returnDict}, context_instance=RequestContext(request))

#
# Displays or modifies session data
#
# Accepts one required parameter:
#    sessionID: the session id
#
@user_passes_test(admin_test)
def editSession(request, sessionID):
    try:
        currentSession = Session.objects.filter(id=sessionID)[0]
    except IndexError:  # Session does not exist in the database, send 404
        return HttpResponseNotFound()

    template_name = "main/admin/editSession.html"

    # Build current zones dictionary
    returnDictZones = buildZonesList()

    # Build current session dictionary
    returnDictSession = model_to_dict(currentSession, fields=[field.name for field in currentSession._meta.fields])

    # Build a list of RMSIDs
    currentSessionRMSID = currentSession.rmsID
    currentSessionRMSID_list = currentSessionRMSID.split(",")

    # Join the data into a common dictionary
    returnDict = dict()
    returnDict['zones'] = returnDictZones
    returnDict['session'] = returnDictSession
    returnDict['rmsIDList'] = currentSessionRMSID_list

    if request.method == 'POST':
        # User submitted an edit request
        if request.POST['method'] == "edit":
            form = SessionForm(data=request.POST)

            if form.is_valid():
                errors = form._errors.setdefault(NON_FIELD_ERRORS, ErrorList())

                currentSession.date = request.POST['date']
                currentSession.time = request.POST['time']
                currentSession.zone = request.POST['zone']

                # If the new capacity (maxID) is smaller than the current number of registered students (countID),
                # send an error flag and return to the form
                if int(request.POST['capacity']) < int(currentSession.countID):
                    errors.append(u'The new capacity cannot be smaller than the current number of registered students (' + str(currentSession.countID) + u').')

                    return render_to_response(template_name, {'form': form, 'data': returnDict}, context_instance=RequestContext(request))
                else:
                    currentSession.maxID = request.POST['capacity']

                currentSession.save()

                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                else:
                    errors.append(u'Please enable cookies and try again.')
                    return render_to_response(template_name, {'form': form, 'data': returnDict}, context_instance=RequestContext(request))

        # User submitted a delete request
        elif request.POST['method'] == "delete":
            currentSession.delete()

            # Redirect to the session list
            return HttpResponseRedirect(reverse('list-sessions'))

        # Unusual request, send 403 response
        else:
            return HttpResponseForbidden()

    # User is viewing session details
    else:
        form = SessionForm(
            initial={'date': currentSession.date,
                     'time': currentSession.time,
                     'capacity': currentSession.maxID,
                     'zone': currentSession.zone}
        )

    request.session.set_test_cookie()

    return render_to_response(template_name, {'form': form, 'data': returnDict}, context_instance=RequestContext(request))

#
# Lists zone data
#
@user_passes_test(admin_test)
def listZones(request):
    template_name = "main/admin/listZones.html"

    # Build zones dictionary - empty zones are included
    currentLocations = Location.objects.all()
    returnDictZones = dict()
    for i in range(11):
        zone_location_list = []
        for locationInstance in currentLocations:
            if locationInstance.zoneNum == i:
                locationDict = dict()
                locationDict['name'] = locationInstance.name
                locationDict['key'] = locationInstance.key
                zone_location_list.append(locationDict)

        returnDictZones[i] = dict()
        returnDictZones[i]['title'] = 'Zone ' + str(i)
        returnDictZones[i]['key'] = i
        returnDictZones[i]['locations'] = zone_location_list

    # Build unassigned locations list - locations which have not been assigned a zone
    null_location_list = []
    for locationInstance in currentLocations:
        if locationInstance.zoneNum is None:
            null_locationDict = dict()
            null_locationDict['name'] = locationInstance.name
            null_locationDict['key'] = locationInstance.key
            null_location_list.append(null_locationDict)

    returnDictNullLocations = dict()
    returnDictNullLocations['title'] = 'Unassigned Locations'
    returnDictNullLocations['key'] = 'null'
    returnDictNullLocations['locations'] = null_location_list

    return render_to_response(template_name, {'zones': returnDictZones, 'locations': returnDictNullLocations}, context_instance=RequestContext(request))

#
# Displays zone text for generated PDFs and handles text change.
#
@user_passes_test(admin_test)
def pdfZoneText(request):
    template_name = "main/admin/zoneText.html"

    # Build current zones dictionary
    zones = buildZonesList()

    # Build dictionary of initial text
    initialDict = dict()
    for i in range(11):
        initialDict['zone' + str(i)] = Zone.objects.get(number=i).text
    initialDict['length'] = request.session['settings']['session_length']

    if request.method == 'POST':
        form = ZoneTextForm(data=request.POST)
        if form.is_valid():
            length = WebsiteSettings.objects.get(id=1)
            length.session_length = request.POST['length']
            request.session['settings']['session_length'] = request.POST['length']
            length.save()
            for i in range(11):
                zone = Zone.objects.get(number=i)
                zone.text = request.POST['zone' + str(i)]
                zone.save()

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

    else:
        form = ZoneTextForm(
            initial=initialDict
        )

    request.session.set_test_cookie()

    return render_to_response(template_name, {'form': form, 'zones': zones}, context_instance=RequestContext(request))

#
# Displays fields for uploading map PDFs.
#
@user_passes_test(admin_test)
def pdfMapUpload(request):
    template_name = "main/admin/mapUpload.html"

    if request.method == 'POST':
        form = PDFMapForm(request.POST, request.FILES)
        if form.is_valid():
            # Continuing PCV Students - Parking Info
            handle_uploads(request, 'co_pcv_map', 'co_pcv_parking_info.pdf')
            # Transfer PCV Students - Parking Info
            handle_uploads(request, 'trans_pcv_map', 'trans_pcv_parking_info.pdf')
            # PCV Students - Loop Navigation Info
            handle_uploads(request, 'pcv_loop', 'pcv_loop_nav_info.pdf')
            # Continuing Cerro Students - Parking Info
            handle_uploads(request, 'co_cerro_map', 'co_cerro_parking_info.pdf')
            # Freshman/Transfer Cerro Students - Parking Info
            handle_uploads(request, 'fresh_trans_cerro_map', 'fresh_trans_cerro_parking_info.pdf')

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
    else:
        form = PDFMapForm()

    request.session.set_test_cookie()

    return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))

#
# A helper function for the pdfMapUpload view
#
def handle_uploads(request, key, filename):
    upload_dir = 'documents'
    upload_full_path = os.path.join(settings.MEDIA_ROOT, upload_dir)

    if not os.path.exists(upload_full_path):
        os.makedirs(upload_full_path)

    if key in request.FILES:
        upload = request.FILES[key]
        dest = open(os.path.join(upload_full_path, filename), 'wb')
        for chunk in upload.chunks():
            dest.write(chunk)
        dest.close()
#
# Searches for a student's reservation data given either a Cal Poly ID or an RMS ID or displays search forms
#
@user_passes_test(admin_test)
def search(request):
    template_name = "main/admin/search.html"
    alias_search_form = aliasSearchForm
    rms_search_form = RMSSearchForm

    # Build current zones dictionary
    zones = buildZonesList()

    # Handle Search Action
    if request.method == "POST":
        # Searching by Cal Poly Alias, grab the rmsID
        if request.POST['lookup_type'] == 'alias':
            form_alias = alias_search_form(data=request.POST)
            form_rmsID = rms_search_form()
            data = None

            if form_alias.is_valid():
                errors = form_alias._errors.setdefault(NON_FIELD_ERRORS, ErrorList())
                try:
                    rmsID = get_rmsID(request.POST['alias'])
                except ObjectDoesNotExist:
                    errors.append(u'The alias provided does not match University Housing records.')
                    return render_to_response(template_name, {'form_alias': form_alias, 'form_rmsID': form_rmsID, 'data': data, 'zones': zones}, context_instance=RequestContext(request))

                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

                try:
                    currentSessions = Session.objects.all()
                    for sessionInstance in currentSessions:
                        if str(rmsID) in sessionInstance.rmsID.split(","):
                            data = model_to_dict(sessionInstance, fields=[field.name for field in sessionInstance._meta.fields])
                            data['rmsID'] = rmsID
                            break
                except (RuntimeError, TypeError, NameError):
                    data = None

                if not data:
                    errors.append(u'The alias provided did not return any session matches.')
                    return render_to_response(template_name, {'form_alias': form_alias, 'form_rmsID': form_rmsID, 'data': data, 'zones': zones}, context_instance=RequestContext(request))

        if request.POST['lookup_type'] == 'rmsID':
            form_alias = alias_search_form()
            form_rmsID = rms_search_form(data=request.POST)
            data = None

            if form_rmsID.is_valid():
                errors = form_rmsID._errors.setdefault(NON_FIELD_ERRORS, ErrorList())
                try:
                    rmsID = request.POST['rmsID']
                    get_alias(rmsID)
                except ObjectDoesNotExist:
                    errors.append(u'The RMS ID provided does not match University Housing records.')
                    return render_to_response(template_name, {'form_alias': form_alias, 'form_rmsID': form_rmsID, 'data': data, 'zones': zones}, context_instance=RequestContext(request))

                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

                try:
                    currentSessions = Session.objects.all()
                    for sessionInstance in currentSessions:
                        if str(rmsID) in sessionInstance.rmsID.split(","):
                            data = model_to_dict(sessionInstance, fields=[field.name for field in sessionInstance._meta.fields])
                            data['rmsID'] = rmsID
                            break
                except (RuntimeError, TypeError, NameError):
                    data = None

                if not data:
                    errors.append(u'The RMS ID provided did not return any session matches.')
                    return render_to_response(template_name, {'form_alias': form_alias, 'form_rmsID': form_rmsID, 'data': data, 'zones': zones}, context_instance=RequestContext(request))

    else:
        form_alias = alias_search_form()
        form_rmsID = rms_search_form()
        data = None

    request.session.set_test_cookie()

    return render_to_response(template_name, {'form_alias': form_alias, 'form_rmsID': form_rmsID, 'data': data, 'zones': zones}, context_instance=RequestContext(request))

#
# A control panel which contains website settings
#
@user_passes_test(admin_test)
def controlPanel(request):
    template_name = "main/admin/controlPanel.html"

    if request.method == 'POST':
        form = TermCodeForm(data=request.POST)
        if form.is_valid():
            term = WebsiteSettings.objects.get(id=1)
            term.term_code = request.POST['term_code']
            request.session['settings']['term_code'] = request.POST['term_code']
            term.save()

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

    # User is viewing session details
    else:
        form = TermCodeForm(
            initial={'term_code': request.session['settings']['term_code']}
        )

    request.session.set_test_cookie()

    return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))

#
# Displays statistics about the current reservation data
#
@user_passes_test(admin_test)
def statistics(request):
    template_name = "main/admin/statistics.html"

    dateDict = dict()
    dateList = []

    currentSessions = Session.objects.all()
    for sessionInstance in currentSessions:
        if sessionInstance.date not in dateList:
            dateList.append(sessionInstance.date)

    numDates = len(dateList)
    dateList.sort()
    dateList.reverse()
    for i in range(numDates):
        currentDate = dateList.pop()
        dateDict[i] = dict()
        dateDict[i]['display'] = currentDate
        dateDict[i]['value'] = datetime.datetime.strftime(currentDate, '%Y-%m-%d')

    return render_to_response(template_name, {'dates':dateDict}, context_instance=RequestContext(request))

#
# Framed by statistics - displays the first chart
#
@user_passes_test(admin_test)
def statsChart0(request, date):

    template_name = "main/admin/statsChart0.html"
    return render_to_response(template_name, genCharts(date), context_instance=RequestContext(request))

#
# Framed by statistics - displays the second chart
#
@user_passes_test(admin_test)
def statsChart1(request, date):
    # genCharts is stupid inefficient, and creates both chart0 and chart1 on each call. This sleep
    # prevents it from double-writing objects to the DB.
    time.sleep(2)
    template_name = "main/admin/statsChart1.html"
    return render_to_response(template_name, genCharts(date), context_instance=RequestContext(request))

#
# Full page view - displays the first chart
#
@user_passes_test(admin_test)
def statsChart0Full(request, date):

    template_name = "main/admin/statsChart0Full.html"
    return render_to_response(template_name, genCharts(date), context_instance=RequestContext(request))

#
# Full page view - displays the second chart
#
@user_passes_test(admin_test)
def statsChart1Full(request, date):
    # genCharts is stupid inefficient, and creates both chart0 and chart1 on each call. This sleep
    # prevents it from double-writing objects to the DB.
    time.sleep(2)
    template_name = "main/admin/statsChart1Full.html"
    return render_to_response(template_name, genCharts(date), context_instance=RequestContext(request))


#
# Prune the session DB of any duplicate rmsIDs
#
@user_passes_test(admin_test)
def pruneSessionDuplicates(request):
    currentSessions = Session.objects.all()
    for sessionInstance in currentSessions:

        if sessionInstance.rmsID != "":
            rmsList = sessionInstance.rmsID.split(",")

            d = {}
            for x in rmsList:
                d[x] = 1
            rmsList = list(d.keys())

            rmsIDStr = ""
            for rmsIDInst in rmsList:
                if rmsIDStr != "":
                    rmsIDStr = rmsIDStr + "," + rmsIDInst
                else:
                    rmsIDStr = rmsIDInst

            sessionInstance.rmsID = rmsIDStr
            sessionInstance.countID = len(rmsList)
            sessionInstance.save()

        else:
            sessionInstance.countID = 0
            sessionInstance.save()

    return HttpResponseRedirect(reverse('list-sessions'))


