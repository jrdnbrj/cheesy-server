from graphene import ObjectType, Field, String

from ...services.settings_service import get_settings
from ..type import SettingsType

from datetime import datetime


class Query(ObjectType):
    get_settings = Field(SettingsType)
    get_datetime = Field(String)

    def resolve_get_settings(parent, info):
        return get_settings()

    def resolve_get_datetime(parent, info):
        return datetime.utcnow()
