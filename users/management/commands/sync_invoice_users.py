from django.core.management.base import BaseCommand
from users.models import SubLinkUser
from django.db import connections
import datetime as dt

class Command(BaseCommand):
    help = "Fully sync usernames and telegram IDs from mirzabot.invoice to mini_app.SubLinkUser"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("\n[⚠️] Flushing SubLinkUser table..."))
        deleted, _ = SubLinkUser.objects.all().delete()
        self.stdout.write(self.style.WARNING(f"  • {deleted} old records deleted.\n"))

        self.stdout.write(self.style.NOTICE("[🔄] Fetching data from mirzabot.invoice..."))

        with connections['mirzabot'].cursor() as cursor:
            cursor.execute("SELECT username, id_user FROM invoice")
            results = cursor.fetchall()

        total = len(results)
        added = 0
        skipped_empty = 0
        added_usernames = set()

        for index, (username, telegram_id) in enumerate(results, start=1):
            if not username or username.strip() == "":
                skipped_empty += 1
                continue

            username = username.strip()
            if username in added_usernames:
                continue  # skip internal duplicates

            SubLinkUser.objects.create(
                username=username,
                telegram_id=telegram_id,
                link=""
            )
            added_usernames.add(username)
            added += 1
            self.stdout.write(self.style.SUCCESS(f"[✅]-({index}) Added {username} (Telegram ID: {telegram_id})"))

        # Summary
        self.stdout.write(self.style.SUCCESS(f"\n[🎯] Sync Complete"))
        self.stdout.write(f"  • Total fetched: {total}")
        self.stdout.write(f"  • Added: {added}")
        self.stdout.write(f"  • Skipped (empty usernames): {skipped_empty}")
        