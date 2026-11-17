from __future__ import annotations

from typing import Any

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Manager for the custom User model.

    Email is used as the authentication identifier.
    """

    def create_user(
        self,
        email: str,
        username: str,
        last_name: str,
        password: str | None = None,
        **extra_fields: Any,
    ):
        """
        Create and persist a regular user.

        Args:
            email: Unique email address.
            username: User's display name.
            last_name: User's family name.
            password: Raw password to hash.
            extra_fields: Additional model fields.

        Returns:
            The created user instance.

        Raises:
            ValueError: If email is missing.
        """
        if not email:
            raise ValueError(_("Email address is required."))

        email = self.normalize_email(email).strip().lower()

        user = self.model(
            email=email,
            username=username.strip(),
            last_name=last_name.strip(),
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user