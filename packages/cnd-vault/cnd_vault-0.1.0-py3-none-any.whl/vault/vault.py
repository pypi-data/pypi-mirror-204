from vault.__version__ import (
    __version__,
)
import hvac
from vault.vault_base import VaultBase
from vault.v1 import V1
from vault.v2 import V2


class Vault(V1, V2):
    def __init__(self, host_url, role_id, secret_id, _print):
        super().__init__(host_url, role_id, secret_id, _print)
        self.v1 = V1(host_url, role_id, secret_id, _print)
        self.v2 = V2(host_url, role_id, secret_id, _print)
        self._print.info_c(f"CndVault Version {__version__}")
        
#     def write_v1(self, path, secret):
#         client = self._connect()
#         client.kv.default_kv_version = 1
#         create_response = client.secrets.kv.v1.create_or_update_secret(path, secret=secret)
#         return True
        
#     def list_v1(self, path):
#         client = self._connect()
#         client.kv.default_kv_version = 1
#         print('++++++')
#         list = client.secrets.kv.v1.list_secrets(path=path)
#         print(list)
#         print('--------')
#         return list
        
#     def read_v1(self, path):
#         client = self._connect()
#         client.kv.default_kv_version = 1
#         return client.kv.read_secret(path=path)
        
#     def read_v2(self, path):
#         client = self._connect()
#         list_response = client.secrets.kv.v2.list_secrets(path='path')
# #        client.kv.default_kv_version = 1
# #        return client.kv.read_secret(path=path)
# ##        secret_version_response = client.secrets.kv.v2.read_secret_version(path=path)
