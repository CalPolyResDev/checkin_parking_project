"""
.. module:: checkin_parking.apps.core.views
   :synopsis: Checkin Parking Reservation Core Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""
import sys
import traceback

from django.template.context import RequestContext
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)

        # TODO: Add Session data to context

        return context


def handler500(request):
    """500 error handler which includes ``request`` in the context."""

    from django.template import loader
    from django.http import HttpResponseServerError

    template = loader.get_template('500.html')
    context = RequestContext(request)

#     exc_type, exc_value, exc_traceback = sys.exc_info()
#     lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
#     message = lines[-1]
#
#     context['exception_text'] = message
    try:
        raise
    except Exception as exc:
        context['exception_text'] = str(exc)

    return HttpResponseServerError(template.render(context))
