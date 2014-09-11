from hbs_parking.rmsConnector.utils import get_address, get_full_name
from hbs_parking.rmsConnector.forms import RMSAuthenticationForm
from models import Session, Location
from django.forms.util import ErrorList
from django.forms.forms import NON_FIELD_ERRORS
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
import re, datetime
from hbs_parking.main.utils_session import loadSettings, home_check_session_placement, home_build_dict
from django.core.exceptions import ObjectDoesNotExist

#
# hbs_parking general views
# These views control both administrator and student authentication and displays the index
#
# Author: Alex Kavanaugh
# Email:  kavanaugh.development@outlook.com
#

def home(request):
    template_name = "main/index.html"
    returnDict = dict()

    request.session['settings'] = loadSettings()

    # Build current zones dictionary
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

    # Check if any PCV sessions aren't such
    currentPCVSessions = list(Session.objects.all())
    currentPCVSessions = [session for session in currentPCVSessions if home_check_session_placement(session, 'PCV')]

    # Check if any CV sessions aren't such
    currentCVSessions = list(Session.objects.all())
    currentCVSessions = [session for session in currentCVSessions if home_check_session_placement(session, 'CV')]


    returnDict['PCV'] = home_build_dict(currentPCVSessions)
    returnDict['CV'] = home_build_dict(currentCVSessions)

    return render_to_response(template_name, {'data': returnDict}, context_instance=RequestContext(request))


#
# Displays the login form and handles the login action for both admins and students.
# Authentication is done first through ldap. If the user is a student, he/she is then validated through rms.
#
# The user's display name is also set as a session variable upon complete authentication:
#        request.session["user_display_name"]
#
@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request):
    template_name = "main/login.html"
    authentication_form = AuthenticationForm
    rms_authentication_form = RMSAuthenticationForm

    # Load settings
    request.session['settings'] = loadSettings()

    # Check if the user is already authenticated
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))

    # Handle Login Action
    if request.method == "POST":

        # Student is attempting to authenticate
        if request.POST['user_type'] == 'student':
            form_student = rms_authentication_form(data=request.POST)
            form_admin = authentication_form()
            if form_student.is_valid():
                errors = form_student._errors.setdefault(NON_FIELD_ERRORS, ErrorList())

                # Authenticate the user against RMS
                alias = request.POST['alias']
                alias = alias.lower()
                dob = datetime.datetime.strptime(request.POST['dob'], "%m/%d/%Y").date()
                user = authenticate(alias=alias, dob=dob)

                # Check if the student will be living in currently supported communities
                try:
                    lookup = get_address(alias, request.session['settings']['term_code'])
                except ObjectDoesNotExist:
                    lookup = None
                if lookup is not None and (lookup['community'] == 'Poly Canyon Village' or lookup['community'] == 'Cerro Vista'):
                    # Student is verified, log him/her in
                    auth_login(request, user)
                    # Set session variables
                    request.session['user_display_name'] = get_full_name(alias)
                else:
                    errors.append(u'The alias provided does not match University Housing records for either Poly Canyon Village or Cerro Vista.')
                    return render_to_response(template_name, {'form_student': form_student, 'form_admin': form_admin}, context_instance=RequestContext(request))

                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

                # Redirect to main page
                return HttpResponseRedirect(reverse('student-home'))

        # Administrator is attempting to authenticate
        if request.POST['user_type'] == 'admin':
            form_student = rms_authentication_form()
            form_admin = authentication_form(data=request.POST)
            if form_admin.is_valid():
                # Authenticate the user against LDAP
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                auth_login(request, user)

                # Set session variables
                request.session['user_display_name'] = user.get_full_name()
                # Load settings
                request.session['settings'] = loadSettings()

                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

                # Redirect to admin home
                return HttpResponseRedirect(reverse('admin-home'))

    else:
        form_admin = authentication_form()
        form_student = rms_authentication_form()

    request.session.set_test_cookie()

    return render_to_response(template_name, {'form_student': form_student, 'form_admin': form_admin}, context_instance=RequestContext(request))

#
# Logs the user out
#
def logout(request):
    auth_logout(request)
    redirection = reverse('home')
    return HttpResponseRedirect(redirection)
