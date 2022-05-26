from .settings_dev import INSTALLED_APPS, MIDDLEWARE

INSTALLED_APPS += (
    'livereload',
)

MIDDLEWARE += (
    'livereload.middleware.LiveReloadScript',
)
