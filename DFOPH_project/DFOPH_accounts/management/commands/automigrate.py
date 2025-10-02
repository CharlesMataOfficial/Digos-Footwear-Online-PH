# DFOPH_accounts/management/commands/automigrate.py
from django.core.management.base import BaseCommand
from django.core.management import call_command
import traceback
import sys

class Command(BaseCommand):
    help = "Automatically runs makemigrations and migrate for all apps (uses call_command)"

    def add_arguments(self, parser):
        parser.add_argument('--no-makemigrations', action='store_true',
                            help='Skip makemigrations step')
        parser.add_argument('--fake', action='store_true',
                            help='Run migrate --fake')

    def handle(self, *args, **options):
        apps = ['DFOPH_accounts', 'DFOPH_sellers', 'DFOPH_buyers']

        try:
            for app in apps:
                if not options['no_makemigrations']:
                    self.stdout.write(self.style.NOTICE(f"📦 Making migrations for '{app}'"))
                    call_command('makemigrations', app, verbosity=1)

            self.stdout.write(self.style.NOTICE("🔁 Applying all migrations"))
            migrate_args = []
            if options['fake']:
                migrate_args = ['--fake']
            call_command('migrate', *migrate_args, verbosity=1)

            self.stdout.write(self.style.SUCCESS("✅ Done with all migrations!"))
        except Exception:
            self.stdout.write(self.style.ERROR("automigrate: exception occurred"))
            traceback.print_exc(file=sys.stdout)
            raise
