"""Message templates kept separate from provider adapters."""

from __future__ import annotations

from django.utils.translation import gettext as _


OTP_EMAIL_TEMPLATE = "otp_email"
NOTIFICATION_EMAIL_TEMPLATE = "notification_email"



def render_email(template: str, context: dict[str, object]) -> tuple[str, str]:
    """Return `(subject, body)` for an email template."""

    if template == OTP_EMAIL_TEMPLATE:
        subject = str(context.get("subject") or _("Your Eventory verification code"))
        body = _("Your Eventory verification code is {code}.").format(code=context["code"])
        return subject, body
    if template == NOTIFICATION_EMAIL_TEMPLATE:
        subject = str(context.get("subject") or _("Eventory notification"))
        return subject, str(context.get("body", ""))
    raise ValueError(f"Unknown email template: {template}")
