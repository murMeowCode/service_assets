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
                # Запуск RPC сервера
                logger.info("Initializing RPC server thread...")
                from .rpc_server import start_server
                rpc_thread = threading.Thread(
                    target=start_server,
                    daemon=True,
                    name="RPC_Server_Thread"
                )
                rpc_thread.start()
                logger.info("RPC server thread started successfully")

                # Запуск баланс-апдейтера
                logger.info("Initializing Balance Updater thread...")
                from .balance_updater import start_balance_updater_consumer
                balance_thread = threading.Thread(
                    target=start_balance_updater_consumer,
                    daemon=True,
                    name="Balance_Updater_Thread"
                )
                balance_thread.start()
                logger.info("Balance Updater thread started successfully")

            except Exception as e:
                logger.error(f"Failed to start background threads: {str(e)}", exc_info=True)
