from django.apps import AppConfig

class SrcConfig(AppConfig):
    """Django Apps Config class"""

    name = 'project'

    def ready(self) -> None:
        from . import signals
