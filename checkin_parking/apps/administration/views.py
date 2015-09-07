"""
.. module:: checkin_parking.apps.administration.views
   :synopsis: Checkin Parking Reservation Administration Views.

.. moduleauthor:: Thomas Willson <thomas.willson@me.com>

"""

from pathlib import Path

from django.core.urlresolvers import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, UpdateView

from checkin_parking.apps.administration.forms import PDFMapForm

from ...settings.base import MEDIA_ROOT
from ..reservations.models import TimeSlot, ReservationSlot
from .models import AdminSettings


class AdminSettingsUpdateView(UpdateView):
    template_name = 'administration/admin_settings.html'
    model = AdminSettings
    fields = ['reservation_open', 'term_code', 'timeslot_length']
    success_url = reverse_lazy('settings')

    def get_object(self, queryset=None):
        return AdminSettings.objects.get_settings()

    def form_valid(self, form):
        if any(field in form.changed_data for field in ['term_code', 'timeslot_length']) and (TimeSlot.objects.count() or ReservationSlot.objects.count()):
            form.add_error(None, 'All reservations and time slots must be purged before changing the ' + ' or '.join([field.replace('_', ' ') for field in form.changed_data]) + '.')
            return super(AdminSettingsUpdateView, self).form_invalid(form)

        return super(AdminSettingsUpdateView, self).form_valid(form)


class PurgeView(TemplateView):
    template_name = 'administration/purge.html'


class PDFMapUploadView(FormView):
    template_name = "administration/map_upload.html"
    form_class = PDFMapForm
    success_url = reverse_lazy('update_maps')

    def form_valid(self, form):
        upload_dir = 'documents'
        upload_full_path = Path(MEDIA_ROOT).joinpath(upload_dir)

        try:
            upload_full_path.mkdir(parents=True)
        except FileExistsError:
            pass

        filenames = {
            'co_pcv_map': 'co_pcv_parking_info.pdf',
            'trans_pcv_map': 'trans_pcv_parking_info.pdf',
            'pcv_loop': 'pcv_loop_nav_info.pdf',
            'co_cerro_map': 'co_cerro_parking_info.pdf',
            'fresh_trans_cerro_map': 'fresh_trans_cerro_parking_info.pdf'
        }

        for key, filename in filenames.items():
            if key in self.request.FILES:
                upload = self.request.FILES[key]
                filedata = b''.join(upload.chunks())

                dest = open(str(upload_full_path.joinpath(filename)), 'wb')
                dest.write(filedata)
                dest.close()

        return super(FormView, self).form_valid(form)
