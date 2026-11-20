"""Factory/registry that resolves a MessageSender by channel and provider."""

from __future__ import annotations

from django.conf import settings

from app.sms_gateway.interfaces import MessageSender
from app.sms_gateway.provider.email import EmailSender


_CHANNEL_SENDERS: dict[str, type[MessageSender]] = {
    "email": EmailSender,
}

class MessageSenderFactory:
    """Return the configured strategy for a logical channel (`sms` or `email`)."""

    def get(self, channel: str) -> MessageSender:
        """
        Resolve a sender.

        `phone` is treated as `sms` so authentication code can speak in
        identifier-channel terms.
        """

        normalized = "sms" if channel in {"sms", "phone"} else channel

        try:
            sender_cls = _CHANNEL_SENDERS[normalized]
        except KeyError as exc:
            raise ValueError(f"Unknown messaging channel: {channel}") from exc
        return sender_cls()
