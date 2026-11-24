from dataclasses import dataclass

from boxoffice.domain.factories import UserFactory
from boxoffice.domain.repositories import UserRepository


@dataclass(frozen=True)
class RegisterUserCommand:
    email: str
    password: str


class RegisterUserHandler:
    def __init__(self, factory: UserFactory, users: UserRepository):
        self._factory, self._users = factory, users

    def handle(self, cmd: RegisterUserCommand) -> int:
        return self._users.add(self._factory.create(cmd.email, cmd.password)).id
