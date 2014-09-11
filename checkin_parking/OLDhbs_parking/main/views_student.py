from hbs_parking.main.utils_session import buildZonesList
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from django.forms.models import model_to_dict
from models import Session, Location, Zone
from hbs_parking.rmsConnector.utils import get_rmsID, get_full_name, get_address, get_term_type
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from PIL import Image
import datetime

#
# hbs_parking student views
# These views control the display and modification of hbs_parking.main's student pages
#
# Author: Chase Voorhees
# Email:  chase@cjvoorhees.com
# Author: Alex Kavanaugh
# Email : kavanaugh.development@outlook.com
#


#
# The following views are permissions tests - this determines what permissions a user must have to be able to access a view.
# It returns either true or false, based on whether or not the test is passed. This allows for major code reduction by using
# the @user_passes_test decorator.
#
# For more information, see "Limiting Access to Users Who Pass a Test" in chapter 14 of the DjangoBook 2.0
#     http://www.djangobook.com/en/2.0/chapter14/
def reserve_test(user):
    if user.is_authenticated():
        if user.has_reserved:
            return False
        else:
            return True
    return False

def view_reservation_test(user):
    if user.is_authenticated():
        if user.has_reserved:
            return True
        elif user.is_developer or user.is_staff:
            return True
    return False

#
# Allows students to reserve sessions
# Does not display full sessions, past sessions, and sessions outside of currentUser building zone
#
@user_passes_test(reserve_test)
def reserveSession(request):
    # Make sure reservation is open
    if not request.session['settings']['status_is_open']:
        return HttpResponseForbidden()

    template_name = "main/student/reserveSession.html"

    # Hack to allow FR/TR students to see all Cerro session data
    FRTRDoubleZone = False
    building2 = None

    # Figure out what zone currentUser is in
    userID = request.user.username
    try:
        address = get_address(userID, request.session['settings']['term_code'])
        building = address['building']
        community = address['community']
        termType = get_term_type(userID, request.session['settings']['term_code'])
        if community == 'Cerro Vista':
            if termType != 'Continuing':
                FRTRDoubleZone = True
                building2 = 'Cerro Vista (FR/TR)'
    except ObjectDoesNotExist:
        building = None

    # Cycle through the zone list and check if the user's building is in that zone, break if it is
    currentLocations = Location.objects.all()
    for i in range(11):
        returnListZoneX = []
        for locationInstance in currentLocations:
            if locationInstance.zoneNum == i:
                # Account for global zones
                if locationInstance.key == 'cerro_vista_all':
                    returnListZoneX.extend(['Bishop', 'Cabrillo', 'Islay', 'Morro', 'Romauldo', 'Hollister', 'Cerro San Luis'])
                elif locationInstance.key == 'poly_canyon_village_all':
                    returnListZoneX.extend(['Aliso', 'Buena Vista', 'Corralitos', 'Dover', 'Estrella', 'Foxen', 'Gypsum', 'Huasna', 'Inyo'])
                else:
                    returnListZoneX.append(locationInstance.name)
        # If the user's building is in the i'th location[zone] dictionary, break the loop
        if returnListZoneX.count(building) > 0:
            break

    zone = i
    zone2 = -1

    # Cycle again for FR/TR students
    if FRTRDoubleZone:
        currentLocations = Location.objects.all()
        for i in range(11):
            returnListZoneX = []
            for locationInstance in currentLocations:
                if locationInstance.zoneNum == i:
                    # Account for global zones
                    if locationInstance.key == 'cerro_vista_all':
                        returnListZoneX.extend(['Bishop', 'Cabrillo', 'Islay', 'Morro', 'Romauldo', 'Hollister', 'Cerro San Luis'])
                    elif locationInstance.key == 'poly_canyon_village_all':
                        returnListZoneX.extend(['Aliso', 'Buena Vista', 'Corralitos', 'Dover', 'Estrella', 'Foxen', 'Gypsum', 'Huasna', 'Inyo'])
                    else:
                        returnListZoneX.append(locationInstance.name)
            # If the user's building is in the i'th location[zone] dictionary, break the loop
            if returnListZoneX.count(building2) > 0:
                break

        zone2 = i


    # Build current zones dictionary
    returnDictZones = buildZonesList()

    # Build list of current sessions
    currentSessions = list(Session.objects.all())
    currentSessions.sort(key=lambda x: x.date)

    # Build the returnDict of sessions, sorted by date and then time
    # returnDict[0][0], for instance is a session during the first time slot of the first day
    # for which the zone matches currentUser.zone
    currentDate = None
    numDates = 0
    dayList = []
    returnDictSessions = dict()

    for i in range(len(currentSessions)):
        # First pass, set current date
        if currentDate is None:
            currentDate = currentSessions[i].date
        # Date is the same, add object to dayList
        if currentDate == currentSessions[i].date:
            if currentSessions[i].countID < currentSessions[i].maxID and (currentSessions[i].date - datetime.date.today()).total_seconds() > 0:
                if currentSessions[i].zone == zone:
                    dayList.append(currentSessions[i])
                if currentSessions[i].zone == zone2:
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
            returnDictSessions[numDates] = dayDict
            numDates = numDates + 1

            # Create new dayList and add current day to it
            dayList = []
                # Only add the session instance if it matches the user's zone & it's not full
            if currentSessions[i].countID < currentSessions[i].maxID and (currentSessions[i].date - datetime.date.today()).total_seconds() > 0:
                if currentSessions[i].zone == zone:
                    dayList.append(currentSessions[i])
                if currentSessions[i].zone == zone2:
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
            returnDictSessions[numDates] = dayDict

    return render_to_response(template_name, {'data': returnDictSessions, 'zones': returnDictZones}, context_instance=RequestContext(request))

#
# Returns student's current reservation details
#
@user_passes_test(view_reservation_test)
def viewReservation(request):
    template_name = "main/student/viewReservation.html"
    returnDict = dict()

    # Build current zones dictionary
    zones = buildZonesList()
    if not zones:
        zones = None

    userID = request.user.username
    try:
        currentID = get_rmsID(userID)
        community = get_address(userID, request.session['settings']['term_code'])['community']
        termType = get_term_type(userID, request.session['settings']['term_code'])
    except ObjectDoesNotExist:
        currentID = 0
        community = None
        termType = ""
        returnDict['zone'] = 0

    currentSessions = Session.objects.all()
    for sessionInstance in currentSessions:
        if str(currentID) in sessionInstance.rmsID.split(","):
            returnDict = model_to_dict(sessionInstance, fields=[field.name for field in sessionInstance._meta.fields])
            break

    return render_to_response(template_name, {'data': returnDict, 'zones': zones, 'community': community, 'termType':termType}, context_instance=RequestContext(request))

#
# Returns pdfResponse of the student's reservation details
#
@user_passes_test(view_reservation_test)
def printParkingPass(request):
    timeInterval = request.session['settings']['session_length']

    # Gather the student information
    try:
        userID = request.user.username
        name = get_full_name(userID)
        rmsID = get_rmsID(userID)
    except ObjectDoesNotExist:  # An admin is viewing the pass
        userID = request.user.username
        name = request.user.get_full_name()
        rmsID = 000000
        date = datetime.date.today()
        time = datetime.datetime.now().time()
        zone = 0

    # Figure out which session they're registered for
    currentSessions = list(Session.objects.all())
    for sessionInstance in currentSessions:
        if str(rmsID) in list(sessionInstance.rmsID.split(",")):
            date = sessionInstance.date
            time = sessionInstance.time
            zone = sessionInstance.zone
            break

    building = ""
    zoneList = buildZonesList()
    for i in range(len(zoneList[zone]['names'])):
        if i == 0:
            building = zoneList[zone]['names'][i]
        else:
            building = building + " or " + zoneList[zone]['names'][i]

    date_and_time = datetime.datetime.combine(date, time)
    timeString = datetime.datetime.strftime(date_and_time, '%I:%M %p')
    # Pull the leading 0 off of the time if it's there (eg 08:40 AM)
    if time.hour < 10:
        timeString = timeString[1:]
    dateString = datetime.datetime.strftime(date_and_time, '%A, %B %d, %Y')

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=parkingpass.pdf'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=letter)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    # pg 29 Font List
    # http://www.reportlab.com/docs/reportlab-userguide.pdf

    # Dynamic drawTexts (based on user)

    PAGE_WIDTH = 8.5 * inch

    text3_string = dateString
    text3_width = stringWidth(text3_string, "Helvetica-Bold", 24)
    text3 = p.beginText()
    text3.setTextOrigin((PAGE_WIDTH - text3_width) / 2.0, (11 - 7.25) * inch)
    text3.setFont("Helvetica-Bold", 24)
    text3.textLine(text3_string)
    p.drawText(text3)

    text4_string = "Resident: " + name
    text4_width = stringWidth(text4_string, "Helvetica-Bold", 24)
    text4 = p.beginText()
    text4.setTextOrigin((PAGE_WIDTH - text4_width) / 2.0, (11 - 6.8) * inch)
    text4.setFont("Helvetica-Bold", 24)
    text4.textLine(text4_string)
    p.drawText(text4)

    text10 = p.beginText()
    text10.setTextOrigin(0.4 * inch, (11 - 2) * inch)
    text10.setFont("Helvetica", 22)
    text10.textLine(text4_string)
    p.drawText(text10)

    text5_string = "Zone " + str(zone)
    text5_width = stringWidth(text5_string, "Helvetica-Bold", 36)
    text5 = p.beginText()
    text5.setTextOrigin((PAGE_WIDTH - text5_width) / 2.0, (11 - 9.65) * inch)
    text5.setFont("Helvetica-Bold", 36)
    text5.textLine(text5_string)
    p.drawText(text5)

    text6_string = building
    text6_width = stringWidth(text6_string, "Helvetica-Bold", 22)
    text6 = p.beginText()
    text6.setTextOrigin((PAGE_WIDTH - text6_width) / 2.0, (11 - 10.08) * inch)
    text6.setFont("Helvetica-Bold", 22)
    text6.textLine(text6_string)
    p.drawText(text6)

    text2_string = timeString
    text2_width = stringWidth(text2_string, "Helvetica-Bold", 100)
    text2 = p.beginText()
    text2.setTextOrigin((PAGE_WIDTH - text2_width) / 2.0, (11 - 8.75) * inch)
    text2.setFont("Helvetica-Bold", 100)
    text2.textLine(text2_string)
    p.drawText(text2)

    text8_string = "Keep on Dashboard - Valid for " + str(timeInterval) + " Minutes"
    text8_width = stringWidth(text8_string, "Helvetica-Bold", 24)
    text8 = p.beginText()
    text8.setTextOrigin((PAGE_WIDTH - text8_width) / 2.0, (11 - 10.5) * inch)
    text8.setFont("Helvetica-Bold", 24)
    text8.textLine(text8_string)
    p.drawText(text8)

    text7 = p.beginText()
    text7.setTextOrigin(0.4 * inch, (11 - 2.4) * inch)
    text7.setFont("Helvetica", 12)

    if request.session['settings']['mode_is_move_in']:
        text7.textLine("Please follow the parking map to your designated move-in location to receive further directions from")
    else:
        text7.textLine("Please follow the parking map to your designated move-out location to receive further directions from")
    text7.textLine("parking staff. For access to the short-term parking area, please follow the instructions below for the")
    text7.textLine("building you have been assigned. Be sure to bring this page with you.")
    text7.textLine("")

# split currentZoneText at first " " before char70
# then remainder at first " " before char 100
# then again^

    currentZoneText = Zone.objects.get(number=zone).text

    currentIndex = 0
    finalIndex = 0
    while currentIndex != -1:
        currentIndex = currentZoneText.find(" ", currentIndex + 1, 70)
        if (currentIndex != -1):
            finalIndex = currentIndex + 1

    splitZoneTextLine0 = currentZoneText[0:finalIndex]
    currentZoneText = currentZoneText[finalIndex:]

    currentIndex = 0
    finalIndex = 0
    while currentIndex != -1:
        currentIndex = currentZoneText.find(" ", currentIndex + 1, 100)
        if (currentIndex != -1):
            finalIndex = currentIndex + 1

    splitZoneTextLine1 = currentZoneText[0:finalIndex]
    currentZoneText = currentZoneText[finalIndex:]

    currentIndex = 0
    finalIndex = 0
    while currentIndex != -1:
        currentIndex = currentZoneText.find(" ", currentIndex + 1, 100)
        if (currentIndex != -1):
            finalIndex = currentIndex + 1

    splitZoneTextLine2 = currentZoneText[0:]

    text7.textLine(building + " (Zone " + str(zone) + ") - " + splitZoneTextLine0)
    text7.textLine(splitZoneTextLine1)
    text7.textLine(splitZoneTextLine2)

    p.drawText(text7)



    # Static drawTexts (same for each user)

    logo = Image.open("Z:\Projects\hbs_parking\hbs_parking\main\static\images\housing_logo.jpg")

    p.drawInlineImage(logo, .5 * inch, (11 - 1.5) * inch, width=1.75 * inch, height=1 * inch)

    text0 = p.beginText()
    text0.setTextOrigin(3.9 * inch, (11 - .7) * inch)
    text0.setFont("Helvetica-Bold", 20)
    text0.textLine("Cal Poly University Housing")
    p.drawText(text0)

    text1 = p.beginText()
    text1.setTextOrigin(3.05 * inch, (11 - 1.1) * inch)
    text1.setFont("Helvetica-Bold", 20)
    if request.session['settings']['mode_is_move_in']:
        text1.textLine("Move-in Registration Confirmation")
    else:
        text1.textLine("Move-out Registration Confirmation")
    p.drawText(text1)

    text11 = p.beginText()
    text11.setTextOrigin(3.75 * inch, (11 - 1.47) * inch)
    text11.setFont("Helvetica-Oblique", 11)
    if request.session['settings']['mode_is_move_in']:
        text11.textLine("Print and bring this page with you for move-in.")
    else:
        text11.textLine("Print and bring this page with you for move-out.")
    p.drawText(text11)

    text9 = p.beginText()
    text9.setTextOrigin(0.4 * inch, (11 - 4.05) * inch)
    text9.setFont("Helvetica-Bold", 12)
    text9.textLine("After unloading, please move your vehicle from the short-term parking area back to your ")
    text9.textLine("long-term designated parking location, so that other students can access the short-term ")
    text9.textLine("parking area. Your short-term parking pass is valid for " + str(timeInterval) + " minutes during your designated time.")
    p.drawText(text9)

    text12 = p.beginText()
    text12.setTextOrigin(0.4 * inch, (11 - 4.95) * inch)
    text12.setFont("Helvetica", 12)
    text12.textLine("Due to limited parking, only one pass is allowed per student at a time. Additional short-term parking")
    text12.textLine("passes may be obtained upon check-in as space permits. Additional passes are also available if you")
    text12.textLine("are delayed in your travel or you cannot make your specific time.")
    p.drawText(text12)

    text13 = p.beginText()
    text13.setTextOrigin(0.4 * inch, (11 - 5.85) * inch)
    text13.setFont("Helvetica-Bold", 12)
    text13.textLine("Any vehicle parked inappropriately and/or for longer than " + str(timeInterval) + " minutes will be cited or towed away")
    text13.textLine("at owner's expense. No vehicles are permitted on any lawn areas or walkways at any time.")
    text13.textLine("Parking is never permitted in fire lanes and state vehicle spaces.")
    p.drawText(text13)


    p.rect(0.8 * inch, (11 - 9.05) * inch, 6.75 * inch, 1.6 * inch, fill=0)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response
