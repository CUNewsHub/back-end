import json
import os
from ...models import Category, Tag
from django.core.management.base import BaseCommand, CommandError
from src.settings import BASE_DIR, TAGS_FILE


class Command(BaseCommand):
    help = 'Updates the Categories and Tags according to tags_categories.json \
        file under newshub/files'

    def handle(self, *args, **options):
        try:
            with open(os.path.abspath(os.path.join(
                    BASE_DIR,
                    'newshub',
                    'files',
                    TAGS_FILE))) as f:
                data = json.load(f)
                for category in data["categories"]:
                    cat, created = Category.objects.get_or_create(
                        name=category["name"])
                    for tag in category["tags"]:
                        Tag.objects.get_or_create(category=cat, name=tag)

        except IOError:
            raise CommandError(
                "File %s does not exist" % TAGS_FILE)
