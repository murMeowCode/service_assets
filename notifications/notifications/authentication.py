from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .rpc_client import AuthRPCClient
import logging

logger = logging.getLogger(__name__)

class RabbitMQJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token.get('user_id')
        if not user_id:
            raise AuthenticationFailed('Invalid token: missing user_id')
        
        try:
            # Создаем RPC-клиент
            rpc_client = AuthRPCClient()
            response = rpc_client.call(user_id)
            
            if 'error' in response:
                logger.error(f"Auth service error: {response['error']}")
                raise AuthenticationFailed('Internal auth error')
                
            if not response.get('exists'):
                raise AuthenticationFailed('User not found')
                
            if not response.get('is_active', True):
                raise AuthenticationFailed('User is inactive')
            
            # Создаем минимальный объект пользователя
            class SimpleUser:
                def __init__(self, **kwargs):
                    self.id = user_id
                    self.username = kwargs.get('username')
                    self.email = kwargs.get('email')
                    self.is_authenticated = True
                    self.is_active = kwargs.get('is_active', True)
                    self.is_root = kwargs.get('is_root')
                    self.first_name = kwargs.get('first_name')
                    self.last_name = kwargs.get('last_name')
                    self.father_name = kwargs.get('father_name')
                    self.balance = kwargs.get('balance')
                    self.balance_virtual = kwargs.get('balance_virtual')
                    self.vip_level = kwargs.get('vip_level')
            
            return SimpleUser(**response)
            
        except TimeoutError:
            logger.error("Auth service timeout")
            raise AuthenticationFailed('Auth service unavailable')
        except Exception as e:
            logger.error(f"Auth error: {str(e)}")
            raise AuthenticationFailed('Authentication failed')
