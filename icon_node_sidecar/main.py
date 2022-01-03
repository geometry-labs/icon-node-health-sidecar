from time import sleep

import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi_health import health
from loguru import logger
from prometheus_client import start_http_server

from icon_node_sidecar.config import settings
from icon_node_sidecar.metrics import prom_metrics
from icon_node_sidecar.utils.peers import get_peers
from icon_node_sidecar.utils.rpc import get_icx_getLastBlock


def health_check():
    # Get the local block height
    local_block_height = get_icx_getLastBlock("localhost:9000/api/v3")

    # Get top block height
    top_block_height = get_top_block_height()

    if local_block_height + 100 < top_block_height:
        print()

    # Compare threshold

    return


def get_top_block_height(peers: list) -> int:
    top_block_height = 0
    for p in peers[0:20]:
        block_height = get_icx_getLastBlock(p)
        if block_height > top_block_height:
            top_block_height = block_height
    return top_block_height


def main(worker_type: str = None):
    logger.info("Starting metrics server.")
    start_http_server(settings.METRICS_PORT, settings.METRICS_ADDRESS)

    logger.info("Starting cron")
    iter = 0
    peers = []
    while True:
        if iter % 100:
            peers = get_peers({(settings.PEER_SEED_IP, settings.PEER_SEED_ADDRESS)})

        get_top_block_height(peers)
        logger.info("Prep stake ran.")
        prom_metrics.preps_stake_cron_ran.inc()
        sleep(settings.CRON_SLEEP_SEC)


if __name__ == "__main__":
    app = FastAPI(
        title="ICON Governance Service",
        description="...",
        version="v0.1.0",
        openapi_url=f"{settings.DOCS_PREFIX}/openapi.json",
        docs_url=f"{settings.DOCS_PREFIX}",
    )
    api_router = APIRouter()
    app.include_router(api_router, prefix=settings.REST_PREFIX)
    app.add_api_route(settings.HEALTH_PREFIX, health([health_check]))
