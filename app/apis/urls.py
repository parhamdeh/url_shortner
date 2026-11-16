# Django Built-in apps
from django.urls import path, include

# Third Party apps
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

app_name = "api"
url_patterns = [

    # OpenAPI schema
    path(
        route="api/schema/",
        view=SpectacularAPIView.as_view(),
        name="schema"
        ),

    # Swagger UI
    path(
        route="api/docs/",
        view=SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),

    # Users Endpoints
    path(
        route="api/users/",
        view=include("app.users.urls")
    ),

    # Shortner Endpoints
    path(
        route="api/shortner/",
        view=include("app.shortner.urls")
    ),

]
