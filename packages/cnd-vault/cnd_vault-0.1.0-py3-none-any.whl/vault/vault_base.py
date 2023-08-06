from vault.__version__ import (
    __version__,
)
import hvac


class VaultBase():
    def __init__(self, host_url, role_id, secret_id, _print):
        self._print = _print
        self._host_url = host_url
        self._role_id = role_id
        self._secret_id = secret_id
        self.client = None
        
    def _connect(self):
        if self.client is not None:
            return self.client
        self.client = hvac.Client(url=self._host_url, verify=False)
#        self.client.token = "e77b11d3-721f-27b6-30ba-9ada03e36a7b"
        self.client.auth.approle.login(
            role_id=self._role_id,
            secret_id=self._secret_id,
        )
        self._print.info_c(f"Authenticated : {self.client.is_authenticated()}")
        return self.client
