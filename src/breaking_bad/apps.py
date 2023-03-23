from django.apps import AppConfig


class BreakingBadConfig(AppConfig):
    name = 'breaking_bad'
    
    def ready(self) -> None:
        import breaking_bad.signals
