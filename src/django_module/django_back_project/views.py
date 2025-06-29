import json
import logging
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect
# from telegram import Update

# from django_back_project.celery import app
# from django_back_project.settings import DEBUG
# from telegram_bot.dispatcher import dispatcher
# from telegram_bot.main import bot

logger = logging.getLogger(__name__)


# @app.task(ignore_result=True)
# def process_telegram_event(update_json):
#     update = Update.de_json(update_json, bot)
#     dispatcher.process_update(update)


def index(request):
    return HttpResponseRedirect('/tgadmin/')


class TelegramBotWebhookView(View):
    # WARNING: if fail - Telegram webhook will be delivered again.
    # Can be fixed with async celery task execution
    def post(self, request, *args, **kwargs):
        # if DEBUG:
        #     process_telegram_event(json.loads(request.body))
        # else:
        #     # Process Telegram event in Celery worker (async)
        #     # Don't forget to run it and & Redis (message broker for Celery)!
        #     # Locally, You can run all of these services via docker-compose.yml
        #     process_telegram_event.delay(json.loads(request.body))

        # e.g. remove buttons, typing event
        return JsonResponse({"ok": "POST request processed"})

    def get(self, request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "Get request received! But nothing done"})
