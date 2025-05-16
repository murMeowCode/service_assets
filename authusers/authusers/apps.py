from django.apps import AppConfig
import threading
import os

class AuthusersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authusers'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            # Отложенный импорт после полной загрузки Django
            from .rpc_server import start_server
            thread = threading.Thread(target=start_server, daemon=True)
            thread.start()