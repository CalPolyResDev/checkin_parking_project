"""
.. module:: checkin_parking.apps.administration.forms
   :synopsis: Checkin Parking Reservation Administration Forms.

.. moduleauthor:: Thomas Willson <thomas.willson@me.com>

"""

import os

from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms.fields import FileField


class PDFMapForm(Form):
    co_pcv_map = FileField(label='Poly Canyon Village Continuing Student Parking Info', required=False)
    trans_pcv_map = FileField(label='Poly Canyon Village Transfer Student Parking Info', required=False)
    pcv_loop = FileField(label='Poly Canyon Village Loop Navigation Info', required=False)
    co_cerro_map = FileField(label='Cerro Vista Continuing Student Parking Info', required=False)
    fresh_trans_cerro_map = FileField(label='Cerro Vista Freshman/Transfer Student Parking Info', required=False)

    def clean(self):
        cleaned_data = super(PDFMapForm, self).clean()
        for filedata in cleaned_data:
            if cleaned_data[filedata]:
                filename = cleaned_data[filedata].name
                ext = os.path.splitext(filename)[1].lower()
                if ext != '.pdf':
                    raise ValidationError("One or more of the files are not PDF documents.")
        return cleaned_data
