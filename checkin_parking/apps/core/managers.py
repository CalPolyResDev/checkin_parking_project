"""
.. module:: checkin_parking.apps.core.managers
   :synopsis: Checkin Parking Reservation Core Managers.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

from django.db.models.manager import Manager


class DefaultRelatedManager(Manager):
    use_for_related_fields = True

    def __init__(self, select_related=None, prefetch_related=None):
        self._select_related = select_related
        self._prefetch_related = prefetch_related
        super(DefaultRelatedManager, self).__init__()

    def get_queryset(self):
        queryset = super(DefaultRelatedManager, self).get_queryset()

        if self._select_related:
            queryset = queryset.select_related(*self._select_related)

        if self._prefetch_related:
            queryset = queryset.prefetch_related(*self._prefetch_related)

        return queryset
