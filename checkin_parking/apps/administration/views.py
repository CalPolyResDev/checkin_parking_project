'''
Created on Sep 4, 2015

@author: thomaswillson
'''

import os
from pathlib import Path

from django.views.generic.edit import FormView

from checkin_parking.settings.base import MEDIA_ROOT


class pdfMapUpload(FormView):
    template_name = "main/admin/mapUpload.html"

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

        for key, filename in filenames:
            if key in self.request.FILES:
                upload = self.request.FILES[key]
                filedata = b''.join(upload.chunks())

                dest = open(str(upload_full_path.joinpath(filename)), 'wb')
                dest.write(filedata)
                dest.close()

        return super(FormView, self).form_valid(form)
