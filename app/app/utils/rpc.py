import json

import requests

from ..log import logger
from ..settings import settings


def convert_hex_int(hex_string: str) -> int:
    return int(hex_string, 16)


def post_rpc_json(response):
    if response.status_code != 200:
        return None
    return response.json()["result"]


def post_rpc(payload: dict):
    r = requests.post(settings.ICON_NODE_URL, data=json.dumps(payload))

    if r.status_code != 200:
        logger.info(f"Error {r.status_code} with payload {payload}")
        r = requests.post(settings.BACKUP_ICON_NODE_URL, data=json.dumps(payload))
        if r.status_code != 200:
            logger.info(f"Error {r.status_code} with payload {payload} to backup")
        return r

    return r


def get_admin_chain(ip_address: str):
    """Get the response from the admin API."""
    url = f"http://{ip_address}:9000/admin/chain/0x1"

    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException:
        return None

    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_icx_getLastBlock(target_ip):
    payload = {"jsonrpc": "2.0", "method": "icx_getLastBlock", "id": 1234}
    try:
        r = requests.post(target_ip, data=json.dumps(payload), timeout=1)
    except Exception:
        return None

    if r.status_code == 200:
        return json.loads(r.content)["result"]["height"]

    return None
