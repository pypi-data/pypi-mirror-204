from vault.vault_base import VaultBase


class V2(VaultBase):

    def config(self, mount_point):
        client = self._connect()
        kv_configuration = client.secrets.kv.v2.read_configuration(mount_point=mount_point)
        return kv_configuration

    def list(self, mount_point, path):
        client = self._connect()
        list_response = client.secrets.kv.v2.list_secrets(path=path, mount_point=mount_point)
        return list_response

    def read(self, mount_point, path):
        client = self._connect()
        secret_version_response = client.secrets.kv.v2.read_secret_version(path=path, mount_point=mount_point)
        return secret_version_response

    def write(self, mount_point, path, secret):
        client = self._connect()
        result = client.secrets.kv.v2.create_or_update_secret(path=path, secret=secret, mount_point=mount_point)
        return result

    def delete(self, mount_point, path):
        client = self._connect()
        result = client.secrets.kv.v2.delete_metadata_and_all_versions(path=path, mount_point=mount_point)
        return result
