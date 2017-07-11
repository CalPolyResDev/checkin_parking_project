from django.core.management.base import BaseCommand

from ...utils import sync_zone_data


class Command(BaseCommand):

    help = "Sync Building and Community Tables"

    def handle(self, *args, **options):
        sync_zone_data()
