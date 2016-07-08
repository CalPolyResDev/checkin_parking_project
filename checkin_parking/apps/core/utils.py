"""
.. module:: checkin_parking.apps.core.utils
   :synopsis: Checkin Parking Core Utils

.. moduleauthor:: Thomas Willson <thomas.willson@icloud.com>

"""
from rest_framework.routers import DefaultRouter


class DecoratorDefaultRouter(DefaultRouter):

    def __init__(self, decorator):
        self.decorator = decorator

        super().__init__()

    def get_urls(self):
        urls = super().get_urls()

        for url in urls:
            url._callback = self.decorator(url._callback)

        return urls
