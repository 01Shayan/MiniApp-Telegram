from django.db import models


# SubLinkUser Model
class SubLinkUser(models.Model):
    telegram_id = models.BigIntegerField()
    username = models.CharField(max_length=255)
    link = models.URLField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sub_link_user"
        unique_together = ("telegram_id", "username")  # Prevent duplicates
        ordering = ["-id"]

    def __str__(self):
        return f"{self.username} ({self.telegram_id})"

# Telegram User Model
class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    language_code = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = "telegram_user"

    def __str__(self):
        return f"{self.first_name} (@{self.username}) - {self.telegram_id}"



# class TelegramUser(models.Model):
#     telegram_id = models.BigIntegerField(unique=True)
#     username = models.CharField(max_length=255, blank=True, null=True)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255, blank=True, null=True)
#     language_code = models.CharField(max_length=10, blank=True, null=True)

#     class Meta:
#         db_table = "telegram_user"

#     def __str__(self):
#         return f"{self.first_name} (@{self.username}) - {self.telegram_id}"
    

# class TerminalUser(models.Model):
#     telegram_id = models.BigIntegerField(unique=False)
#     username = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         db_table = "terminal_user"

#     def __str__(self):
#         return f"{self.telegram_id} - {self.username}"
    

# class SubLinkUser(models.Model):
#     telegram_id = models.BigIntegerField(unique=False)
#     username = models.CharField(max_length=255, blank=True, null=True)
#     link = models.CharField(max_length=255, blank=True, null=True)
    
#     class Meta:
#         db_table = "sub_link_user"

#     def __str__(self):
#         return f"{self.telegram_id} - {self.username} - {self.link}"

