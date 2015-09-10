"""
.. module:: checkin_parking.apps.reservations.tasks
  :synopsis: Checkin Parking Reservation Reservations Tasks.

.. moduleauthor:: Thomas E. Willson <thomas.willson@me.com>

"""

from django.core import mail
from django.core.mail import EmailMessage

from ...apps.reservations.utils import generate_pdf_file


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


@spool(pass_arguments=True)
def send_confirmation_email(reservation_slot, uri_prefix):
    with mail.get_connection() as connection:
        message = EmailMessage()
        message.connection = connection
        message.subject = 'Checkin Parking Reservation Confirmation'
        message.from_email = 'University Housing <resnet@calpoly.edu>'
        message.to = [reservation_slot.resident.email]
        message.reply_to = ['University Housing <resnet@calpoly.edu>']
        message.attach('Parking Pass.pdf', generate_pdf_file(reservation_slot, uri_prefix), 'application/pdf')
        message.body = 'Hi ' + reservation_slot.resident.full_name + """,

Your parking slot has been successfully reserved and your parking pass is attached. Please be sure to print and place the parking pass on your dashboard.

Reservation Details:

Date: """ + str(reservation_slot.timeslot.date) + """
Start Time: """ + str(reservation_slot.timeslot.time) + """
End Time: """ + str(reservation_slot.timeslot.end_time) + """
Zone: """ + reservation_slot.zone.name + """

If you need to make any changes to your reservation, please visit http://checkin.housing.calpoly.edu.

Thank you,
University Housing
"""
        message.send()
