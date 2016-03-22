"""Command for dumping the flow-graph data."""

import os
import csv
import datetime
from tracking.models import PageVisitor, TrackingMetadata, NewsFeedVisitor
from tracking.models import LoginPageVisitor
from tracking.models import HISTORY, PERSONAL_FEED, TOP_STORIES
from django.core.management.base import BaseCommand
from src.settings import CSV_ROOT


class Command(BaseCommand):
    """Command class."""

    help = 'Updates the Colleges and Subjects objects'

    def handle(self, *args, **options):
        """Handle the command itself."""
        tracking_metadata = TrackingMetadata.load()

        if tracking_metadata.last_dumped_flow_graph is None:
            visitors = PageVisitor.objects.select_subclasses()
        else:
            from_time = tracking_metadata.last_dumped_flow_graph
            visitors = PageVisitor.objects.select_subclasses()\
                                  .filter(visited_time__gte=from_time)

        now = datetime.datetime.now()
        filename = "%s_%s_%s_%s_%s.csv" % (
            now.year, now.month, now.day, now.minute, now.second)

        file_pwd = os.path.join(CSV_ROOT, 'flow-graph-dump', filename)

        with open(file_pwd, 'w') as csv_file:
            fieldnames = ['session_key', 'user_id', 'visited_time',
                          'page_type', 'page_id', 'page_verbose_name']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            for visitor in visitors:
                row = {}
                row['session_key'] = visitor.session_key
                if visitor.user is not None:
                    row['user_id'] = visitor.user.id
                else:
                    row['user_id'] = None

                row['visited_time'] = visitor.visited_time

                if isinstance(visitor, NewsFeedVisitor):
                    row['page_type'] = visitor.page_type
                    if visitor.newsfeed_type == HISTORY:
                        row['page_id'] = 0
                    elif visitor.newsfeed_type == PERSONAL_FEED:
                        row['page_id'] = 1
                    elif visitor.newsfeed_type == TOP_STORIES:
                        row['page_id'] = 2

                    row['page_verbose_name'] = visitor.newsfeed_type
                elif isinstance(visitor, LoginPageVisitor):
                    row['page_type'] = visitor.page_type
                    row['page_id'] = None
                    row['page_verbose_name'] = None
                else:
                    row['page_type'] = visitor.page_type
                    row['page_id'] = visitor.obj.id
                    row['page_verbose_name'] = visitor.obj.__unicode__()

                csv_writer.writerow(row)

            tracking_metadata.last_dumped_flow_graph = now
            tracking_metadata.save()
