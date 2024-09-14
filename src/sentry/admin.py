from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from sqladmin import ModelView, action

from src.admin import last_activity_format
from src.database import LocalSession
from src.sentry.models import Alert, Installation
from src.sentry.services import AlertService


class InstallationAdmin(ModelView, model=Installation):
    column_list = (
        Installation.org_slug,
        Installation.is_active,
        Installation.last_activity,
        Installation.activity_counter,
    )
    column_default_sort = [(Installation.created, True)]
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


class AlertAdmin(ModelView, model=Alert):
    column_list = (
        Alert.title,
        Alert.description,
        Alert.sentry_hook_resource,
        Alert.error_message,
        Alert.created,
    )
    column_default_sort = [(Alert.created, True)]
    column_formatters = {Alert.created: last_activity_format}
    column_searchable_list = (
        Alert.title,
        Alert.description,
        Alert.sentry_hook_resource,
        Alert.update,
        Alert.error_message,
    )
    column_sortable_list = (
        Alert.title,
        Alert.description,
        Alert.sentry_hook_resource,
        Alert.update,
        Alert.error_message,
        Alert.created,
    )
    form_columns = (
        Alert.title,
        Alert.description,
        Alert.sentry_hook_resource,
        Alert.update,
        Alert.error_message,
    )
    can_edit = False

    @action(
        name="test_run",
        label="Test run",
        add_in_detail=True,
    )
    async def test_run(self, request: Request):
        pks = request.query_params.get("pks", "").split(",")
        if pks:
            async with LocalSession(expire_on_commit=False) as session:
                await AlertService(session).test_run(pks)
        referer = request.headers.get("Referer")
        if referer:
            return RedirectResponse(referer)
        return RedirectResponse(request.url_for("admin:list", identity=self.identity))
