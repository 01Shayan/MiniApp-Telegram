from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import redirect
from django.core.management import call_command
from users.models import SubLinkUser, TelegramUser
from urllib.parse import unquote


@admin.register(SubLinkUser)
class SubLinkUserAdmin(admin.ModelAdmin):
    list_display = ("username", "telegram_id", "link")
    search_fields = ("username",)
    list_filter = ("username",)
    change_list_template = "admin/sublinkuser_changelist.html"

    actions = ["update_subscription_links_action"]

    @admin.action(description="2️⃣ Update Subscription Links (Selected Users)")
    def update_subscription_links_action(self, request, queryset):
        selected_users = list(queryset.values_list("username", flat=True))
        if not selected_users:
            self.message_user(request, "⚠️ No users selected.", level=messages.WARNING)
            return
        try:
            call_command("update_links", users=",".join(selected_users))
            self.message_user(request, f"✅ Updated links for {len(selected_users)} users.")
        except Exception as e:
            self.message_user(request, f"❌ Error updating links: {e}", level=messages.ERROR)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("sync-invoice-users/", self.admin_site.admin_view(self.sync_invoice_users), name="sync-invoice-users"),
            path("sync-and-update-users/", self.admin_site.admin_view(self.sync_and_update_links), name="sync-and-update-users"),
            path("update-selected-users/", self.admin_site.admin_view(self.update_selected_links), name="update-selected-users"),
        ]
        return custom_urls + urls

    def sync_invoice_users(self, request):
        try:
            call_command("sync_invoice_users")
            self.message_user(request, "✅ Synced users from invoice.")
        except Exception as e:
            self.message_user(request, f"❌ Error syncing users: {e}", level=messages.ERROR)
        return redirect("admin:users_sublinkuser_changelist")

    def sync_and_update_links(self, request):
        try:
            call_command("sync_and_update_links")
            self.message_user(request, f"✅ Synced & updated all users ({len(SubLinkUser.objects.all())}).")
        except Exception as e:
            self.message_user(request, f"❌ Error syncing & updating: {e}", level=messages.ERROR)
        return redirect("admin:users_sublinkuser_changelist")

    def update_selected_links(self, request):
        users = request.GET.get("users")
        if not users:
            self.message_user(request, "⚠️ No users passed to update.", level=messages.WARNING)
            return redirect("admin:users_sublinkuser_changelist")

        usernames = unquote(users).split(",")
        try:
            call_command("update_links", users=",".join(usernames))
            self.message_user(request, f"✅ Updated links for {len(usernames)} users.")
        except Exception as e:
            self.message_user(request, f"❌ Error updating links: {e}", level=messages.ERROR)
        return redirect("admin:users_sublinkuser_changelist")
    
@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "username", "first_name", "last_name", "language_code")
    search_fields = ("telegram_id", "username", "first_name", "last_name")
    # list_filter = ("telegram_id", "username", "first_name", "last_name", "language_code")
