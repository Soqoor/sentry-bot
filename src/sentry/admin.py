from sqladmin import ModelView

from src.admin import last_activity_format
from src.sentry.models import Installation


class InstallationAdmin(ModelView, model=Installation):
    column_list = (
        Installation.org_slug,
        Installation.is_active,
        Installation.last_activity,
        Installation.activity_counter,
    )
    column_formatters = {Installation.last_activity: last_activity_format}
    column_searchable_list = (
        Installation.org_slug,
        Installation.owner_id,
    )
    column_sortable_list = (
        Installation.last_activity,
        Installation.activity_counter,
    )
    can_create = False
    can_edit = False
