from rest_framework.throttling import AnonRateThrottle


class PublicThrottle(AnonRateThrottle):
    """
    Throttle anonymous users for public API endpoints.
    """

    rate = "10/minute"