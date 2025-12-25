from client import MikroTikClient
from config import (
    ROUTERS,
    MT_USERNAME,
    MT_PASSWORD,
    MT_SSH_PORT,
    MT_SSH_KEY,
)


def get_router_clients():
    clients = {}

    for name, ip in ROUTERS.items():
        clients[name] = MikroTikClient(
            host=ip,
            username=MT_USERNAME,
            password=MT_PASSWORD,
            port=MT_SSH_PORT,
            ssh_key=MT_SSH_KEY,
        )

    return clients
