import json

from src.chats.services import ChatService
from src.sentry.handlers.base import BaseSentryHandler
from src.sentry.schemas import AlertCreate
from src.sentry.services import AlertService, SentryService
from src.sentry.utils import clean_output


class AlertSentryHandler(BaseSentryHandler):
    chat_slug_setting_name = "telegram_bot_chat_key"  # Same field name should be set up in action_schema

    async def handle(self):
        alert = AlertCreate(update=json.dumps(self.update), sentry_hook_resource=self.sentry_hook_resource)
        try:
            alert.title = self.get_title()[:255]
            alert.description = self.get_description()[:255]
            await self._handle()
        except Exception as e:
            alert.error_message = str(e)[:255]
        finally:
            await AlertService(self.db).create_alert(alert)

    async def _handle(self):
        await SentryService(db=self.db).log_sentry_activity(installation_id=self.update["installation"]["uuid"])

        chat_slug = self.get_chat_slug()
        chat = await ChatService(db=self.db).get_by_chat_slug(chat_slug=chat_slug)
        if chat and chat.is_active:
            text = self.create_alert_message()
            await self.bot.send_message(chat_id=chat.chat_id, text=text)
            await ChatService(db=self.db).log_sentry_activity(chat_slug=chat_slug)

    def create_alert_message(self):
        title = self.get_title()
        description = self.get_description() or "No description"
        triggered_rule = self.get_triggered_rule()
        web_url = self.get_web_url()

        message_parts = [
            f'<b><a href="{web_url}">{title}</a></b>',
            f"\n<blockquote>{description}</blockquote>",
            f"\n<i>{triggered_rule}</i>",
        ]
        return "".join(message_parts)

    def get_chat_slug(self):
        raise NotImplementedError()

    def get_title(self):
        raise NotImplementedError()

    def get_description(self):
        raise NotImplementedError()

    def get_triggered_rule(self):
        raise NotImplementedError()

    def get_web_url(self):
        raise NotImplementedError()


class EventAlertSentryHandler(AlertSentryHandler):

    def get_chat_slug(self):
        for setting in self.update["data"]["issue_alert"]["settings"]:
            if setting["name"] == self.chat_slug_setting_name:
                return setting["value"]
        raise Exception("No chat key found")

    @clean_output
    def get_title(self):
        return (
            self.update["data"]["event"].get("metadata", {}).get("type")
            or self.update["data"]["event"]["title"].split(": ")[0]
        )

    @clean_output
    def get_description(self):
        return self.update["data"]["event"].get("metadata", {}).get("value") or ": ".join(
            self.update["data"]["event"]["title"].split(": ")[1:]
        )

    @clean_output
    def get_triggered_rule(self):
        return self.update["data"]["triggered_rule"]

    def get_web_url(self):
        return self.update["data"]["event"]["web_url"]


class MetricAlertSentryHandler(AlertSentryHandler):

    def get_chat_slug(self):
        for trigger in self.update["data"]["metric_alert"]["alert_rule"]["triggers"]:
            for action in trigger["actions"]:
                for setting in action["settings"]:
                    if setting["name"] == self.chat_slug_setting_name:
                        return setting["value"]
        raise Exception("No chat key found")

    @clean_output
    def get_title(self):
        icon_mapping = {"critical": "🟥 ", "warning": "🟨 ", "resolved": "🟩 "}
        return icon_mapping.get(self.update["action"]) + self.update["data"]["description_title"]

    @clean_output
    def get_description(self):
        return self.update["data"]["description_text"]

    @clean_output
    def get_triggered_rule(self):
        return self.update["data"]["metric_alert"]["alert_rule"]["name"]

    def get_web_url(self):
        return self.update["data"]["web_url"]
