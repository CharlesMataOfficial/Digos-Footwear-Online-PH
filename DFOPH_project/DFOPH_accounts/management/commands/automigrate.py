from django.core.management.base import BaseCommand
import subprocess

class Command(BaseCommand):
    help = 'Automatically runs makemigrations and migrate for all apps'

    def handle(self, *args, **options):
        apps = ['DFOPH_accounts', 'DFOPH_sellers', 'DFOPH_buyers']  

        for app in apps:
            self.stdout.write(self.style.NOTICE(f"📦 Making migrations for '{app}'"))
            subprocess.call(['python', 'manage.py', 'makemigrations', app])

        self.stdout.write(self.style.NOTICE("🔁 Applying all migrations"))
        subprocess.call(['python', 'manage.py', 'migrate'])

        self.stdout.write(self.style.SUCCESS("✅ Done with all migrations!"))
