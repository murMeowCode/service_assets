from django.apps import AppConfig
import threading
import os
import logging

logger = logging.getLogger(__name__)

class AuthusersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authusers'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            try:
                logger.info("Initializing RPC server thread...")
                from .rpc_server import start_server
                thread = threading.Thread(
                    target=start_server,
                    daemon=True,
                    name="RPC_Server_Thread"
                )
                thread.start()
                logger.info("RPC server thread started successfully")
            except Exception as e:
                logger.error(f"Failed to start RPC server: {str(e)}", exc_info=True)