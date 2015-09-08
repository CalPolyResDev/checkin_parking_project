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

        self.fields["name"].error_messages = {'required': 'A zone name is required.'}
        self.fields["capacity"].error_messages = {'required': 'A capacity is required.'}
        self.fields["community"].error_messages = {'required': 'A community is required.'}
        self.fields["buildings"].error_messages = {'required': 'At least one building must be selected.'}

        self.fields["capacity"].readonly = True
        self.fields["community"].widget.attrs['autocomplete'] = "off"
        self.fields["buildings"].help_text = ""

    class Meta:
        model = Zone
        fields = ['name', 'capacity', 'community', 'buildings']
