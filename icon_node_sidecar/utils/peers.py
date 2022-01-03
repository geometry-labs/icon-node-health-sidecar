from time import sleep

import requests

from icon_node_sidecar.config import settings
from icon_node_sidecar.log import logger
from icon_node_sidecar.metrics import prom_metrics
from icon_node_sidecar.utils.rpc import get_admin_chain, get_icx_getLastBlock


def p2p_to_rpc_address(p2p_address):
    return p2p_address.split(":")[0], "9000"


def get_prep_address_peers(ip_address: str = "52.26.81.40"):
    admin_metrics = get_admin_chain(ip_address=ip_address)

    peers = []
    for peer in admin_metrics["module"]["network"]["p2p"]["friends"]:
        peers.append({"ip_address": peer["addr"], "public_key": peer["id"]})

    return peers


def scrape_peers(peers):
    neighbor_peers = []
    for peer in peers:
        neighbor_peers.append(get_prep_address_peers(peer["ip_address"].split(":")[0]))
    return neighbor_peers


def get_peers(peer_set: set, added_peers: list = None):
    """
    Function that takes in a set with a tuple of the ip and node_address as a seed to
    then call that node's orphan peers, call those nodes
    """
    if added_peers is None:
        added_peers = []

    old_peer_count = len(added_peers)

    for i in peer_set.copy():
        if i[0] not in added_peers:
            admin_metrics = get_admin_chain(ip_address=i[0])
            added_peers.append(i[0])
        else:
            continue

        if admin_metrics is None:
            continue

        for peer in admin_metrics["module"]["network"]["p2p"]["orphanages"]:

            peer_item = (peer["addr"].split(":")[0], peer["id"])

            if peer_item not in peer_set:
                peer_set.add(peer_item)

    if old_peer_count == len(added_peers):
        return peer_set
    else:
        return get_peers(peer_set, added_peers=added_peers)
