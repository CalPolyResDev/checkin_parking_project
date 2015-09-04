"""
.. module:: checkin_parking.pdfs.view
   :synopsis: Checkin Parking PDFViews.

.. moduleauthor:: Thomas Willson <thomas.willson@me.com>

"""

from pathlib import Path

from django.http.response import HttpResponse
from django.template.context import Context
from django.template.loader import get_template
from django.views.generic.base import TemplateView
import trml2pdf

from checkin_parking.settings.base import MEDIA_ROOT


class ParkingPassVerificationView(TemplateView):
    template_name = 'pdfs/parking_pass_verification.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)

        parking_pass = {
            'valid': False
        }

        context['parking_pass'] = parking_pass

        return context


class ParkingPassPDFView(TemplateView):

    def render_to_response(self, context, **response_kwargs):
        template = get_template('pdfs/parking_pass.rml')

        parking = {
            'date': 'Wednesday, September 8, 2015',
            'start': '2:00PM',
            'end': '2:40PM',
            'building': 'Huasna',
            'zone': '5',
        }

        context = Context({
            'resident_name': 'Fred Smith',
            'cal_poly_logo_path': Path(MEDIA_ROOT).joinpath('pdf_assets/cp_logo.gif'),
            'parking': parking,
            'qr_code_url': 'www.calpoly.edu',
        })
        source_xml = template.render(context)
        pdf_data = trml2pdf.parseString(source_xml)

        response = HttpResponse()
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'filename=parkingpass.pdf'

        response.write(pdf_data)

        return response
