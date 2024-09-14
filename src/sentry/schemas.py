from typing import Optional

from pydantic import BaseModel


class InstallationCreateUpdate(BaseModel):
    installation_id: str
    is_active: Optional[bool] = True
    org_slug: Optional[str] = ""
    auth_token: Optional[str] = ""
    refresh_token: Optional[str] = ""
    owner_id: Optional[int] = None


class AlertCreate(BaseModel):
    title: Optional[str] = ""
    description: Optional[str] = ""
    sentry_hook_resource: str
    update: str
    error_message: Optional[str] = ""
