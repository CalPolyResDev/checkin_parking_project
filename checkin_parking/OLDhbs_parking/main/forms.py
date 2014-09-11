from django.forms.forms import NON_FIELD_ERRORS
from models import Location
from django import forms
import datetime
import os

#
# hbs_parking forms
#
# Author: Alex Kavanaugh
# Email:  kavanaugh.development@outlook.com
#

def buildChoices(required=True):
    # Build zones choices
    currentLocations = Location.objects.all()
    zoneList = []
    uniqueList = []
    for i in range(11):
        for locationInstance in currentLocations:
            if locationInstance.zoneNum == i:
                zoneList.append(i)

    # Make the choices list unique
    for zone in zoneList:
        if zone not in uniqueList:
            uniqueList.append(zone)

    zoneList = uniqueList

    # Build Choices
    CHOICES = []
    if not required:
        CHOICES.extend([("", "")])
    for zone in zoneList:
        CHOICES.extend([(str(zone), str(zone))])

    return CHOICES

class TermCodeForm(forms.Form):
    term_code = forms.IntegerField(label='Term Code', min_value=0, max_value=9999)

class PDFMapForm(forms.Form):
    co_pcv_map = forms.FileField(label='Poly Canyon Village Continuing Student Parking Info', required=False)
    trans_pcv_map = forms.FileField(label='Poly Canyon Village Transfer Student Parking Info', required=False)
    pcv_loop = forms.FileField(label='Poly Canyon Village Loop Navigation Info', required=False)
    co_cerro_map = forms.FileField(label='Cerro Vista Continuing Student Parking Info', required=False)
    fresh_trans_cerro_map = forms.FileField(label='Cerro Vista Freshman/Transfer Student Parking Info', required=False)

    def clean(self):
        cleaned_data = super(PDFMapForm, self).clean()
        for filedata in cleaned_data:
            if cleaned_data[filedata] is not None:
                name = cleaned_data[filedata].name
                ext = os.path.splitext(name)[1]
                ext = ext.lower()
                if ext != '.pdf':
                    raise forms.ValidationError("One or more of the files are not PDF documents.")
        return cleaned_data

class aliasSearchForm(forms.Form):
    alias = forms.CharField(label='Cal Poly Alias', max_length=8, error_messages={'required': 'An alias is required'})

class RMSSearchForm(forms.Form):
    rmsID = forms.IntegerField(label='RMS ID', min_value=0, max_value=999999, error_messages={'required': 'An RMS ID is required', 'max_value': 'Invalid RMS ID', 'min_value': 'Invalid RMS ID'})

class ZoneTextForm(forms.Form):
    length = forms.IntegerField(label='Session Length (Minutes)', error_messages={'required': 'A session length is required'})
    zone0 = forms.CharField(label='Zone 0', widget=forms.Textarea, max_length=285, required=False)
    zone1 = forms.CharField(label='Zone 1', widget=forms.Textarea, max_length=285, required=False)
    zone2 = forms.CharField(label='Zone 2', widget=forms.Textarea, max_length=285, required=False)
    zone3 = forms.CharField(label='Zone 3', widget=forms.Textarea, max_length=285, required=False)
    zone4 = forms.CharField(label='Zone 4', widget=forms.Textarea, max_length=285, required=False)
    zone5 = forms.CharField(label='Zone 5', widget=forms.Textarea, max_length=285, required=False)
    zone6 = forms.CharField(label='Zone 6', widget=forms.Textarea, max_length=285, required=False)
    zone7 = forms.CharField(label='Zone 7', widget=forms.Textarea, max_length=285, required=False)
    zone8 = forms.CharField(label='Zone 8', widget=forms.Textarea, max_length=285, required=False)
    zone9 = forms.CharField(label='Zone 9', widget=forms.Textarea, max_length=285, required=False)
    zone10 = forms.CharField(label='Zone 10', widget=forms.Textarea, max_length=285, required=False)

class SessionForm(forms.Form):
    date = forms.DateField(label='Date', input_formats=['%Y-%m-%d'], error_messages={'required': 'A date is required'})
    time = forms.TimeField(label='Time', input_formats=['%H:%M:%S'], error_messages={'required': 'A time is required'})
    capacity = forms.IntegerField(label='Capacity', error_messages={'required': 'A capacity is required'})
    zone = forms.TypedChoiceField(choices=buildChoices(), coerce=int, label='Zone', error_messages={'required': 'A zone is required'})

class addSessionForm(forms.Form):
    start_time = forms.TimeField(label='Start Time', input_formats=['%H:%M:%S'], error_messages={'required': 'A start time is required'})
    end_time = forms.TimeField(label='End Time', input_formats=['%H:%M:%S'], error_messages={'required': 'An end time is required'})
    interval = forms.IntegerField(label='Minute Interval', error_messages={'required': 'An interval is required'})
    capacity = forms.IntegerField(label='Capacity', error_messages={'required': 'A capacity is required'})
    zone0 = forms.TypedChoiceField(choices=buildChoices(), coerce=int, label='Zone', error_messages={'required': 'At least one zone is required'})
    zone1 = forms.TypedChoiceField(choices=buildChoices(required=False), coerce=int, label='Zone', required=False)
    zone2 = forms.TypedChoiceField(choices=buildChoices(required=False), coerce=int, label='Zone', required=False)
    zone3 = forms.TypedChoiceField(choices=buildChoices(required=False), coerce=int, label='Zone', required=False)
    zone4 = forms.TypedChoiceField(choices=buildChoices(required=False), coerce=int, label='Zone', required=False)

    date0 = forms.DateField(label='Date', input_formats=['%Y-%m-%d'], error_messages={'required': 'At least one date is required'})
    date1 = forms.DateField(label='Date', input_formats=['%Y-%m-%d'], required=False)
    date2 = forms.DateField(label='Date', input_formats=['%Y-%m-%d'], required=False)
    date3 = forms.DateField(label='Date', input_formats=['%Y-%m-%d'], required=False)
    date4 = forms.DateField(label='Date', input_formats=['%Y-%m-%d'], required=False)

    error_messages = {
        'time_conflict': u"The start time must be before the end time.",
        'interval_conflict': u"The minute interval cannot be greater than "
                              "the time slot (end time - start time).",
    }

    def clean(self):
        cleaned_data = super(addSessionForm, self).clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        interval = cleaned_data.get("interval")

        if start_time and end_time and interval:
            currentTimeDelta = datetime.datetime.combine(datetime.date.today(), end_time) - datetime.datetime.combine(datetime.date.today(), start_time)

            # Check to make sure start_time is before end_time
            if currentTimeDelta.total_seconds() < 0:
                raise forms.ValidationError(self.error_messages['time_conflict'])

            # Check to make sure the minute interval isn't bigger than the time slot
            if int(interval) > currentTimeDelta.total_seconds() / 60:
                raise forms.ValidationError(self.error_messages['interval_conflict'])

        return cleaned_data
