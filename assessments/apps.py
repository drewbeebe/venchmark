from django.apps import AppConfig


class AssessmentsConfig(AppConfig):
    name = 'assessments'
    label = 'assessments'

    def ready(self):
        print("importing signals...")
        import assessments.signals
