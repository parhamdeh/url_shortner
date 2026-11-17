from __future__ import annotations

from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.users.managers import UserManager
from app.utils.models import BaseModel


class User(AbstractBaseUser, BaseModel):
    """
    Custom user model for the URL Shortener application.

    Authentication:
        Users authenticate using their unique email address.

    Profile:
        Includes username, last name, profile photo, and birth date.

    Security:
        Passwords are hashed using Django's password hashing system.
        """

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=_("Username"),
        help_text=_("Unique username for the user."),
    )

    last_name = models.CharField(
        max_length=150,
        verbose_name=_("Last name"),
        help_text=_("User's family name."),
    )

    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name=_("Email address"),
        help_text=_("Unique email address used for authentication."),
    )

    profile_photo = models.ImageField(
        upload_to="users/profile_photos/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "webp"],
            ),
        ],
        verbose_name=_("Profile photo"),
        help_text=_("Optional profile picture."),
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Birth date"),
        help_text=_("Optional date of birth."),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "last_name"]

    class Meta:
        """Database configuration for the User model."""

        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ("-created_at",)

    def __str__(self) -> str:
        """Return a readable representation of the user."""
        return self.email

    def save(self, *args, **kwargs):
        """Normalize email and username before saving."""
        if self.email:
            self.email = self.email.strip().lower()

        if self.username:
            self.username = self.username.strip()

        return super().save(*args, **kwargs)