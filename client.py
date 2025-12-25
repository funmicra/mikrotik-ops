import paramiko
from paramiko import SSHException, AuthenticationException


class MikroTikClient:
    def __init__(
        self,
        host: str,
        username: str,
        password: str | None = None,
        port: int = 22,
        ssh_key: str | None = None,
        timeout: int = 10,
    ):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.ssh_key = ssh_key
        self.timeout = timeout
        self.client = None

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy()
            )

            if self.ssh_key:
                key = paramiko.RSAKey.from_private_key_file(self.ssh_key)
                self.client.connect(
                    hostname=self.host,
                    port=self.port,
                    username=self.username,
                    pkey=key,
                    timeout=self.timeout,
                )
            else:
                self.client.connect(
                    hostname=self.host,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    timeout=self.timeout,
                )

        except (SSHException, AuthenticationException) as exc:
            raise RuntimeError(
                f"SSH connection failed to {self.host}: {exc}"
            ) from exc

    def close(self):
        if self.client:
            self.client.close()
            self.client = None

    def call(self, command: str):
        """
        Execute a RouterOS CLI command over SSH.
        Returns stdout as string.
        """
        if not self.client:
            raise RuntimeError("Not connected to router")

        stdin, stdout, stderr = self.client.exec_command(command)

        err = stderr.read().decode().strip()
        if err:
            raise RuntimeError(f"Router error: {err}")

        return stdout.read().decode().strip()

    @property
    def keys(self):
        if not self.client:
            raise RuntimeError("Not connected to router")
        return RouterKeys(self)
