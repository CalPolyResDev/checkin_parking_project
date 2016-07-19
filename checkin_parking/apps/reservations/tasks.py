"""
.. module:: checkin_parking.apps.reservations.tasks
  :synopsis: Checkin Parking Reservation Reservations Tasks.

.. moduleauthor:: Thomas E. Willson <thomas.willson@me.com>

"""

from django.core import mail
from django.core.mail import EmailMessage
from django.utils import formats

from ..administration.models import AdminSettings
from .utils import generate_verification_url, generate_pdf_file


# Emulate spool decorator in order to not cause an error when running locally.
# The extra layer of wrapping is necessary to properly handle decorator arguments.
try:
    from uwsgidecorators import spool
except:
    def spool(**kwargs):
        def wrap(f):
            def wrapped_f(*args):
                f(*args)
            wrapped_f.spool = f
            return wrapped_f
        return wrap


def send_confirmation_email(reservation_slot, request):
    verification_url = generate_verification_url(reservation_slot, request)
    send_confirmation_email_spooler.spool(reservation_slot, verification_url)


@spool(pass_arguments=True)
def send_confirmation_email_spooler(reservation_slot, verification_url):  # Needs uri_prefix to generate absolute url. Requests can't be pickled.
    with mail.get_connection() as connection:
        message = EmailMessage()
        message.connection = connection
        message.subject = 'Your Mustang Move-in Pass'
        message.from_email = 'University Housing <resnet@calpoly.edu>'
        message.to = [reservation_slot.resident.email]
        message.reply_to = ['University Housing <resnet@calpoly.edu>']
        message.attach('Mustang Move-in Pass.pdf', generate_pdf_file(reservation_slot, verification_url), 'application/pdf')
        message.body = 'Hello ' + reservation_slot.resident.full_name + """,

Your Cal Poly Fall move-in arrival time has been successfully reserved and your Mustang Move-in Pass is attached.

My Reservation:

Date: """ + formats.date_format(reservation_slot.timeslot.date) + """
Start Time: """ + formats.time_format(reservation_slot.timeslot.time) + """
End Time: """ + formats.time_format(reservation_slot.timeslot.end_time) + """
Zone: """ + reservation_slot.zone.name + """

Please arrive on your designated day and time. This will help ensure a convenient move-in experience.

If you need to edit your reservation, go to: http://checkin.housing.calpoly.edu. You can edit your reservation until """ + formats.date_format(AdminSettings.objects.get_settings().reservation_close_day) + """.

Please finalize your travel plans based on your final reservation.

Go Mustangs!
University Housing
"""
        message.send()
