from pydantic import BaseModel


class CreateOrUpdateInstallation(BaseModel):
    installation_id: str
    org_slug: str
    auth_token: str = ""
    refresh_token: str = ""
