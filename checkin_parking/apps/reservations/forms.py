"""
.. module:: checkin_parking.apps.reservations.forms
   :synopsis: Checkin Parking Reservation Reservation Forms.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from datetime import datetime, date

from django.core.exceptions import ValidationError
from django.forms.fields import DateField, TimeField, ChoiceField, BooleanField
from django.forms.forms import Form
from django.forms.models import ModelMultipleChoiceField

from ..administration.models import AdminSettings
from ..zones.models import Zone
from .models import CLASS_LEVEL_CHOICES, CLASS_LEVELS


class GenerateReservationsForm(Form):
    date = DateField(label="Date")
    start_time = TimeField(label='Start Time', input_formats=['%H:%M'], error_messages={'required': 'A start time is required'})
    end_time = TimeField(label='End Time', input_formats=['%H:%M'], error_messages={'required': 'An end time is required'})
    class_level = ChoiceField(label='Class Level', choices=CLASS_LEVEL_CHOICES, initial=CLASS_LEVELS.index("Freshman/Transfer/Continuing"), error_messages={'required': 'A class level is required'})
    out_of_state = BooleanField(label='Out of State?', required=False)
    assisted_move_in = BooleanField(label='Assisted move in?', required=False)
    zones = ModelMultipleChoiceField(queryset=Zone.objects.all(), error_messages={'required': 'At least one zone must be selected. If there are no zones from which to choose, please create one.'})

    error_messages = {
        'time_conflict': "The start time must be before the end time.",
        'interval_conflict': "The time window must be greater than the set timeslot length ({length} Minutes)",
    }

    def __init__(self, *args, **kwargs):
        super(GenerateReservationsForm, self).__init__(*args, **kwargs)

        self.fields["class_level"].widget.attrs['autocomplete'] = "off"
        self.fields["zones"].help_text = ""

    def clean(self):
        cleaned_data = super(GenerateReservationsForm, self).clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time:
            time_delta = datetime.combine(date.today(), end_time) - datetime.combine(date.today(), start_time)

            # Check to make sure start_time is before end_time
            if time_delta.total_seconds() < 0:
                raise ValidationError(self.error_messages['time_conflict'], code="code")

            timeslot_length = AdminSettings.objects.get_settings().timeslot_length

            # Check to make sure the minute interval isn't bigger than the time slot
            if timeslot_length > time_delta.total_seconds() / 60:
                raise ValidationError(self.error_messages['interval_conflict'].format(length=timeslot_length), code="interval_conflict")

        return cleaned_data
