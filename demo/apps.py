# Custom translateable app name
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class DemoConfig(AppConfig):
    name = "demo"
    verbose_name = _("demo")
