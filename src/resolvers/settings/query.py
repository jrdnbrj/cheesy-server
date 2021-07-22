from graphene import ObjectType
from graphene import Field

from ...services.settings_service import get_settings
from ..type import SettingsType


class Query(ObjectType):
    get_settings = Field(SettingsType)

    def resolve_get_settings(parent, info):
        return get_settings()
