"""
.. module:: checkin_parking.core.routers
   :synopsis: Checkin Parking Reservation Core Database Routers.

.. moduleauthor:: Kyle Dodson <kdodson@caloply.edu>
.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""


class CommonRouter(object):
    """Routes all common models to the correct database."""

    ALIAS = "common"
    APP_NAME = "core"
    MODELS = ('community', 'building')

    def _app(self, model):
        """ A shortcut to retrieve the provided model's application label.

        :param model: A model instance from which to retrieve information.
        :type model: model
        :returns: The provided model's app label.

        """

        return model._meta.app_label

    def _mod(self, model):
        """ A shortcut to retrieve the provided model's module name, a lower-cased version of its object name.

        :param model: A model instance from which to retrieve information.
        :type model: model
        :returns: The provided model's module name.

        """

        return model._meta.module_name

    def db_for_read(self, model, **hints):
        """Routes database read requests to the database only if the requested model belongs to a model in this application's MODELS list."""

        if self._app(model) == self.APP_NAME and self._mod(model) in self.MODELS:
            return self.ALIAS
        return None

    def db_for_write(self, model, **hints):
        """Routes database write requests to the database only if the requested model belongs to a model in this application's MODELS list."""

        if self._app(model) == self.APP_NAME and self._mod(model) in self.MODELS:
            return self.ALIAS
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Provides no constraints on relationships."""

        return None

    def allow_migrate(self, db, model):
        """Provides no constraints on table synchronization."""

        return None
