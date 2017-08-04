from django.core.management.base import BaseCommand

from ...utils import sync_user_data


class Command(BaseCommand):

    help = "Sync Residents from RMS"

    def handle(self, *args, **options):
        sync_user_data()
