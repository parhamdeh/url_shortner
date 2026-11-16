"""
Database configuration for the Django project.

This module initializes the `DATABASES` setting using environment variables
loaded through the project's environment handler. PostgreSQL is used as the
primary database backend, and all connection parameters—such as host, port,
username, password, and database name—are sourced from the environment to
ensure secure and flexible configuration across development, staging,
and production environments.

Environment Variables:
    POSTGRES_USER: Database username.
    POSTGRES_PASSWORD: Database password.
    POSTGRES_HOST: Host address of the PostgreSQL server.
    POSTGRES_PORT: Port on which the database service is running.
    POSTGRES_DB: Name of the target PostgreSQL database.
"""

from config.settings.env import env

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": env.str("POSTGRES_HOST"),
        "PORT": env.int("POSTGRES_PORT"),
        "NAME": env.str("POSTGRES_DB"),
    }
}
