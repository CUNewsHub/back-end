import json
import os
from ...models import Feedback
from django.core.management.base import BaseCommand, CommandError
from src.settings import BASE_DIR, FEEDBACK_FILE


class Command(BaseCommand):
    help = 'Updates the feedback options, deletes the old ones'

    def handle(self, *args, **options):
        try:
            with open(os.path.abspath(os.path.join(
                    BASE_DIR,
                    'newshub',
                    'files',
                    FEEDBACK_FILE))) as f:
                data = json.load(f)
                Feedback.objects.all().delete()

                for feedback in data["feedback_options"]:
                    Feedback.objects.create(name=feedback)
        except IOError:
            raise CommandError(
                "File %s does not exist" % FEEDBACK_FILE)
