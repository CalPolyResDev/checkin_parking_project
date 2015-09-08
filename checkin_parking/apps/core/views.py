"""
.. module:: checkin_parking.apps.core.views
   :synopsis: Checkin Parking Reservation Core Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""
import logging

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
    context_string = ''
    for k, v in context.flatten().items():
        context_string += str(k) + ': ' + str(v)

    print(context_string)

    logger = logging.getLogger('raven')
    logger.info(context_string)

    RequestContext

    return HttpResponseServerError(template.render(context))
