from django.core.management.base import BaseCommand
import time
from django.db import connection
from django.db.utils import OperationalError



class Command(BaseCommand):
    help = "Wait for postgres database to be ready "

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = False
        while not db_conn:
            try:
                connection.ensure_connection()
                db_conn = True
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))

