from src.chats.services import ChatService
from src.sentry.handlers.base import BaseSentryHandler


class AlertSentryHandler(BaseSentryHandler):

    async def handle(self):

        title = (
            self.update["data"]["event"].get("metadata", {}).get("type")
            or self.update["data"]["event"]["title"].split(": ")[0]
        )
        description = self.update["data"]["event"].get("metadata", {}).get("value") or ": ".join(
            self.update["data"]["event"]["title"].split(": ")[1:]
        )
        chat_slug = self.update["data"]["issue_alert"]["settings"][0]["value"]
        triggered_rule = self.update["data"]["triggered_rule"]
        web_url = self.update["data"]["event"]["web_url"]

        message_parts = [
            f'<b><a href="{web_url}">{title}</a></b>',
            f"\n{description}" or "",
            f"\n\n<i>{triggered_rule}</i>",
        ]
        text = "".join(message_parts)
        chat = await ChatService(db=self.db).get_by_chat_slug(chat_slug=chat_slug)
        await self.bot.send_message(chat_id=chat.chat_id, text=text)
