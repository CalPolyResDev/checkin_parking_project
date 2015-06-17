"""
.. module:: checkin_parking.zones.forms
   :synopsis: Checkin Parking Reservation Zone Forms.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.forms.models import ModelForm

from .models import Zone


class ZoneForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ZoneForm, self).__init__(*args, **kwargs)

        self.fields["number"].error_messages = {'required': 'A zone number is required.'}
        self.fields["community"].error_messages = {'required': 'A community is required.'}
        self.fields["buildings"].error_messages = {'required': 'At least one building must be selected.'}

        self.fields["community"].widget.attrs['autocomplete'] = "off"
        self.fields["buildings"].help_text = ""

    class Meta:
        model = Zone