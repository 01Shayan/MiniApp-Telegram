from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import SubLinkUser, TelegramUser
import json
import logging

logger = logging.getLogger(__name__)

def fetch_user_links(telegram_id):
    """Fetch all links for a given telegram_id, sorted by latest first."""
    return SubLinkUser.objects.filter(telegram_id=telegram_id).order_by("-id")

@csrf_exempt
def store_user_info(request):
    """Stores Telegram user info and returns all associated subscription links."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=405)

    try:
        data = json.loads(request.body)
        telegram_id = data.get("id")

        if not telegram_id:
            return JsonResponse({"error": "Missing Telegram ID."}, status=400)

        # Save user info to TelegramUser model
        TelegramUser.objects.update_or_create(
            telegram_id=telegram_id,
            defaults={
                "username": data.get("username"),
                "first_name": data.get("first_name"),
                "last_name": data.get("last_name"),
                "language_code": data.get("language_code"),
            }
        )

        # Fetch links by telegram_id
        links_qs = fetch_user_links(telegram_id)
        links = [{"username": l.username, "link": l.link} for l in links_qs]

        if not links:
            logger.warning(f"No links found for Telegram ID: {telegram_id}")

        return JsonResponse({
            "id": telegram_id,
            "username": data.get("username", ""),
            "first_name": data.get("first_name", ""),
            "last_name": data.get("last_name", ""),
            "language_code": data.get("language_code", ""),
            "links": links,
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format."}, status=400)
    except Exception as e:
        logger.exception("Unexpected error in store_user_info")
        return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)

def home(request):
    return render(request, "index.html")
