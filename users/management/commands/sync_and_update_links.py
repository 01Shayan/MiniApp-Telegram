from django.core.management.base import BaseCommand
from django.core.management import call_command
from users.models import SubLinkUser
from django.db import connections
import datetime as dt

class Command(BaseCommand):
    help = "Sync from invoice and then update all links in one step."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("\n[🔁] Starting sync and update process...\n"))

        # Step 1: Flush old SubLinkUser data
        deleted_count, _ = SubLinkUser.objects.all().delete()
        self.stdout.write(self.style.WARNING(f"[🧹] Deleted {deleted_count} old SubLinkUser entries."))

        # Step 2: Sync from mirzabot.invoice
        with connections['mirzabot'].cursor() as cursor:
            cursor.execute("SELECT username, id_user FROM invoice")
            results = cursor.fetchall()

        added = 0
        skipped = 0

        for index, (username, telegram_id) in enumerate(results, start=1):
            if not username or username.strip() == "":
                skipped += 1
                continue

            SubLinkUser.objects.create(
                username=username.strip(),
                telegram_id=telegram_id,
                link=""
            )
            added += 1
            self.stdout.write(self.style.SUCCESS(f"[✅]-({index}) Synced {username} (Telegram ID: {telegram_id})"))

        self.stdout.write(self.style.SUCCESS(f"\n[🎯] Sync Complete. Added: {added}, Skipped (empty usernames): {skipped}"))

        # Step 3: Call update_links
        self.stdout.write(self.style.NOTICE("\n[⏳] Running update_links to fetch subscription URLs...\n"))
        call_command("update_links")

        self.stdout.write(self.style.SUCCESS("\n[✅] Sync and update process complete!"))
