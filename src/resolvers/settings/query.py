from graphene import ObjectType
from graphene import Field

from ..type import SettingsType

from ...services.settings_service import get_settings


class Query(ObjectType):
    get_settings = Field(SettingsType)

    def resolve_get_settings(parent, info):
        return get_settings()
