from django.apps import AppConfig


class PayappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payapp'

    def ready(self):
        #start apache thrift server
        from subprocess import Popen
        Popen(['python', './thrift/TimestampHandlerServer/timestamphandlerserver.py'])
