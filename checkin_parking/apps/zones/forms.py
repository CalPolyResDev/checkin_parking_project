"""
.. module:: checkin_parking.zones.forms
   :synopsis: Checkin Parking Reservation Zone Forms.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from clever_selects.form_fields import ModelChoiceField, ChainedModelMultipleChoiceField
from django.forms.models import ModelForm
from django.core.urlresolvers import reverse_lazy

from .models import Zone, Community, Building


class ZoneForm(ModelForm):
    community = ModelChoiceField(queryset=Community.objects.all())
    buildings = ChainedModelMultipleChoiceField('community', reverse_lazy('zones:chained_building'), Building)

    def __init__(self, *args, **kwargs):
        super(ZoneForm, self).__init__(*args, **kwargs)

        self.fields["name"].error_messages = {'required': 'A zone name is required.'}
        self.fields["capacity"].error_messages = {'required': 'A capacity is required.'}
        self.fields["community"].error_messages = {'required': 'A community is required.'}
        self.fields["buildings"].error_messages = {'required': 'At least one building must be selected.'}

        if self.instance and self.instance.id:
            self.fields["capacity"].widget.attrs['readonly'] = True
            self.fields["capacity"].widget.attrs['disabled'] = True
        self.fields["community"].widget.attrs['autocomplete'] = "off"
        self.fields["buildings"].help_text = ""

    def clean_capacity(self):
        capacity = self.cleaned_data.get("capacity", None)

        if self.instance and self.instance.id:
            return self.instance.capacity
        else:
            return capacity

    class Meta:
        model = Zone
        fields = ['name', 'capacity', 'community', 'buildings']
