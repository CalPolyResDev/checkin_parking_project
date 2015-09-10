"""
.. module:: checkin_parking.apps.reservations.utils
  :synopsis: Checkin Parking Reservation {app name} {file name}.

.. moduleauthor:: Thomas E. Willson <thomas.willson@me.com>

"""
from pathlib import Path
import urllib.parse

from django.core.urlresolvers import reverse
from django.template.context import Context
from django.template.loader import get_template
import trml2pdf

from ...settings.base import MEDIA_ROOT


def generate_pdf_file(reservation_slot, uri_prefix):
    context = {}

    parking = {
        'date': reservation_slot.timeslot.date,
        'start': reservation_slot.timeslot.time,
        'end': reservation_slot.timeslot.end_time,
        'zone': reservation_slot.zone.name,
    }

    context['resident_name'] = reservation_slot.resident.full_name
    context['cal_poly_logo_path'] = Path(MEDIA_ROOT).joinpath('pdf_assets/cp_logo.gif')
    context['parking'] = parking
    context['qr_code_url'] = urllib.parse.urljoin(uri_prefix, reverse('verify_parking_pass',
                                                  kwargs={'reservation_id': reservation_slot.id, 'user_id': reservation_slot.resident.id}))

    template = get_template('reservations/parking_pass.rml')

    source_xml = template.render(Context(context))
    pdf_data = trml2pdf.parseString(source_xml)

    return pdf_data
