from vault.vault_base import VaultBase


class V1(VaultBase):
    def read(self, path):
        client = self._connect()
        print(f"Authenticated : {self.client.is_authenticated()}")
        client.kv.default_kv_version = 1
        print(path)
        client.kv.v1.read_secret(path=path)
#        client.kv.v2.read_secret_version(path='hvac')
        return client.kv.read_secret(path=path)
