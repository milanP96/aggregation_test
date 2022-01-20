import datetime
from django.utils import timezone

from django.core.management.base import BaseCommand, CommandError
from aggregator.models import Event

class Command(BaseCommand):
    help = 'Generate events'

    def handle(self, *args, **options):
        now = timezone.now().replace(microsecond=0)


        for x in range(180):
            Event.objects.create(domain="A", timestamp=now - datetime.timedelta(hours=2), requests_number=2)
            Event.objects.create(domain="B", timestamp=now - datetime.timedelta(hours=2), requests_number=1)
            Event.objects.create(domain="C", timestamp=now - datetime.timedelta(hours=2), requests_number=5)

            now = now + datetime.timedelta(minutes=1)