from contexlib import suppress
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "lynkpage.users"
    verbose_name = _("Users")

    def ready(self):
        # ussing contexlib.suppress to ignore the ImportError
        with suppress(ImportError):
            import lynkpage.users.signals  # noqa: F401
