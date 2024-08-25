from sqladmin import ModelView

from src.admin import last_activity_format
from src.chats.models import Chat


class ChatAdmin(ModelView, model=Chat):
    column_list = (
        "name_display",
        Chat.is_active,
        Chat.chat_type,
        Chat.last_activity,
        Chat.user_activity_counter,
        Chat.notify_activity_counter,
    )
    column_formatters = {Chat.last_activity: last_activity_format}
    column_searchable_list = (
        Chat.chat_id,
        Chat.username,
        Chat.first_name,
        Chat.last_name,
        Chat.chat_title,
    )
    column_sortable_list = (
        Chat.last_activity,
        Chat.user_activity_counter,
        Chat.notify_activity_counter,
    )
    can_create = False
    can_edit = False
