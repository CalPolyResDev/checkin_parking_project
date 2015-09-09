"""
.. module:: checkin_parking.apps.reservations.tasks
  :synopsis: Checkin Parking Reservation Reservations Tasks.

.. moduleauthor:: Thomas E. Willson <thomas.willson@me.com>

"""

from django.core import mail
from django.core.mail import EmailMessage

# See: http://projects.unbit.it/uwsgi/wiki/TipsAndTricks#TestingPythonModulesThatUseuwsgidecorators
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
def send_confirmation_email(reservation_slot):
    with mail.get_connection() as connection:
        message = EmailMessage()
        message.connection = connection
        message.subject = 'Checkin Parking Reservation Confirmation'
        message.from_email = 'University Housing <resnet@calpoly.edu>'
        message.to = [reservation_slot.resident.email]
        message.reply_to = ['University Housing <resnet@calpoly.edu>']
        message.body = 'Hi ' + reservation_slot.resident.full_name + """,

Your parking slot has been successfully reserved. Please be sure to print and place your parking pass on your dashboard.

Reservation Details:

Date: """ + str(reservation_slot.timeslot.date) + """
Start Time: """ + str(reservation_slot.timeslot.time) + """
End Time: """ + str(reservation_slot.timeslot.end_time) + """
Zone: """ + reservation_slot.zone.name + """

If you need to make any changes, please visit http://checkin.housing.calpoly.edu.

Thank you,
University Housing
"""
        print(message.to)
        message.send()
