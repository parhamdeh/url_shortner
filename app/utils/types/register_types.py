from dataclasses import dataclass

from app.utils.types.user_types import UserCreateInputType


@dataclass
class RegisterTypes(UserCreateInputType):
    pass


