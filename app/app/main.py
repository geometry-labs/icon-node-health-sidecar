#  Copyright 2022 Geometry Labs, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from loguru import logger

from .checks import router as checks_router
from .settings import settings
from .shared import shared_height
from .utils.peers import get_peers
from .utils.utils import get_top_block_height

iter = 0
peers = []

app = FastAPI(
    title="ICON Node Healthcheck",
    description="ICON Node Healthcheck",
    version="v0.1.0",
    openapi_url=f"{settings.DOCS_ENDPOINT_PREFIX}/openapi.json",
    docs_url=f"{settings.DOCS_ENDPOINT_PREFIX}",
)

app.include_router(checks_router)


@app.on_event("startup")
@repeat_every(seconds=settings.CRON_SLEEP_SEC, logger=logger, wait_first=True)
def scrape_job(peer_height=shared_height):
    global peers
    global iter

    logger.info("Collecting peer information...")
    if iter % 100:
        logger.info("Refreshing peer list...")
        peers = get_peers({(settings.PEER_SEED_IP, settings.PEER_SEED_ADDRESS)})
        logger.info("Peer list refreshed.")

    peer_height.setBest(get_top_block_height(peers))
    logger.info("Peer block heights refreshed.")
    iter += 1
