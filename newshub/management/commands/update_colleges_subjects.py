import json
import os
from ...models import College, Subject
from django.core.management.base import BaseCommand, CommandError
from src.settings import BASE_DIR, COLLEGES_SUBJECTS_FILE


class Command(BaseCommand):
    help = 'Updates the Colleges and Subjects objects'

    def handle(self, *args, **options):
        try:
            with open(os.path.abspath(os.path.join(
                    BASE_DIR,
                    'newshub',
                    'files',
                    COLLEGES_SUBJECTS_FILE))) as f:
                data = json.load(f)
                for college in data["colleges"]:
                    cat, created = College.objects.get_or_create(
                        name=college)

                for subject in data["subjects"]:
                    Subject.objects.get_or_create(name=subject)

        except IOError:
            raise CommandError(
                "File %s does not exist" % COLLEGES_SUBJECTS_FILE)
