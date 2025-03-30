from django.core.management.base import BaseCommand
from users.models import SubLinkUser
from django.conf import settings
import os
import json
import datetime as dt
import requests as req
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Secure credentials
PANEL_USERNAME = os.getenv("PANEL_USERNAME")
PANEL_PASSWORD = os.getenv("PANEL_PASSWORD")
PANEL_DOMAIN = os.getenv("PANEL_DOMAIN")

# Ensure the logs directory exists
LOGS_DIR = settings.BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOGS_DIR / "update_log.json"

# python manage.py update_links --users="Shayan,Test1"
# python manage.py update_links

class Command(BaseCommand):
    help = "Update subscription links for selected or all users"

    def add_arguments(self, parser):
        parser.add_argument("--users", type=str, help="Comma-separated list of usernames to update")

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("\n[🔍] Starting Subscription Link Update Process...\n"))

        token = self.get_token()
        if not token:
            self.stdout.write(self.style.ERROR("[❌] ERROR: Could not retrieve API token. Exiting."))
            return

        user_arg = kwargs.get("users")
        if user_arg:
            all_users = user_arg.split(",")
            self.stdout.write(self.style.SUCCESS(f"[✅] Updating selected users: {', '.join(all_users)}"))
        else:
            all_users = self.get_all_users(token)
            self.stdout.write(self.style.SUCCESS(f"[✅] Updating all {len(all_users)} users."))

        if not all_users:
            self.stdout.write(self.style.ERROR("[❌] ERROR: No users retrieved from API."))
            return

        updates = []

        for index, username in enumerate(all_users, start=1):
            try:
                new_link = self.fetch_subscription_link(username, token)
                if not new_link:
                    self.stdout.write(self.style.WARNING(f"[⚠️]-({index}) Skipping {username}, no new link retrieved."))
                    continue

                sub_user = SubLinkUser.objects.filter(username=username).first()

                if sub_user:
                    old_link = sub_user.link
                    if old_link != new_link:
                        sub_user.link = new_link
                        sub_user.save()
                        self.stdout.write(self.style.SUCCESS(f"[✅]-({index}) Updated link for {username}: {old_link} ➝ {new_link}"))
                        updates.append({
                            "index": index,
                            "username": username,
                            "old_link": old_link,
                            "new_link": new_link,
                            "timestamp": dt.datetime.now().isoformat(),
                        })
                    else:
                        self.stdout.write(self.style.WARNING(f"[⚠️]-({index}) No changes for {username} (same link)."))
                else:
                    SubLinkUser.objects.create(username=username, link=new_link)
                    self.stdout.write(self.style.SUCCESS(f"[✅]-({index}) Created new subscription entry for {username}: {new_link}"))
                    updates.append({
                        "index": index,
                        "username": username,
                        "old_link": "None",
                        "new_link": new_link,
                        "timestamp": dt.datetime.now().isoformat(),
                    })

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"[❌]-({index}) Unexpected error for {username}: {e}"))

        if updates:
            self.log_update(updates)
            self.stdout.write(self.style.SUCCESS("\n[✅] SUCCESS: Selected users updated.\n"))

    def get_token(self):
        url = f"https://{PANEL_DOMAIN}/api/admin/token"
        payload = {"username": PANEL_USERNAME, "password": PANEL_PASSWORD}
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}

        try:
            response = req.post(url, data=payload, headers=headers, timeout=10)
            response.raise_for_status()
            token = response.json().get("access_token")
            if token:
                self.stdout.write(self.style.SUCCESS("[✅] Token received successfully."))
                return token
        except req.RequestException as e:
            self.stdout.write(self.style.ERROR(f"[❌] Failed to get token: {e}"))
            return None

    def get_all_users(self, token):
        url = f"https://{PANEL_DOMAIN}/api/users"
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

        try:
            response = req.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            user_data = response.json()
            all_users = [user["username"] for user in user_data.get("users", []) if user.get("username")]
            return all_users
        except req.RequestException as e:
            self.stdout.write(self.style.ERROR(f"[❌] Error fetching users: {e}"))
            return []

    def fetch_subscription_link(self, username, token):
        url = f"https://{PANEL_DOMAIN}/api/user/{username}"
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

        try:
            response = req.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            sub_url = response.json().get("subscription_url")
            return sub_url
        except req.RequestException as e:
            self.stdout.write(self.style.ERROR(f"[❌] Failed to fetch link for {username}: {e}"))
            return None

    def log_update(self, updates):
        logs = self.load_logs()
        timestamp = dt.datetime.now().isoformat()
        logs[timestamp] = updates

        seven_days_ago = dt.datetime.now() - dt.timedelta(days=7)
        logs = {k: v for k, v in logs.items() if dt.datetime.fromisoformat(k) >= seven_days_ago}

        self.save_logs(logs)

    def load_logs(self):
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as file:
                return json.load(file)
        return {}

    def save_logs(self, logs):
        with open(LOG_FILE, "w") as file:
            json.dump(logs, file, indent=4)
