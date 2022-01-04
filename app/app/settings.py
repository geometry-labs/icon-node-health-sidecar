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

import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DOCS_ENDPOINT_PREFIX: str = "/docs"
    BLOCK_HEIGHT_VARIANCE: int = 50
    PEER_SEED_IP: str = "52.196.159.184"
    PEER_SEED_ADDRESS: str = "hx9c63f73d3c564a54d0eed84f90718b1ebed16f09"
    CRON_SLEEP_SEC: int = 5


if os.environ.get("ENV_FILE", False):
    settings = Settings(_env_file=os.environ.get("ENV_FILE"))
else:
    settings = Settings()
