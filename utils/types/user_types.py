from dataclasses import dataclass


@dataclass
class UserCreateInputType:
    email : str
    password : str
    