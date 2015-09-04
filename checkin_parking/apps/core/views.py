"""
.. module:: checkin_parking.apps.core.views
   :synopsis: Checkin Parking Reservation Core Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)

        # TODO: Add Session data to context

        return context
