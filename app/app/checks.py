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


from typing import Optional

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from .settings import settings
from .shared import shared_height
from .utils.rpc import get_icx_getLastBlock

router = APIRouter()


@router.get("/readyz")
async def node_ready(verbose: Optional[bool] = None, shared_height=shared_height):

    # empty response body for verbose responses
    method_response_body = ""

    # readyz response boolean that we'll bring along as we do our checks
    readyz_status = True

    # get best blockheight
    peer_height = shared_height.getBest()

    # get node's blockheight
    local_height = get_icx_getLastBlock("http://localhost:9000/api/v3")

    # compare best to node (within tolerance)
    if local_height:
        difference = abs(peer_height - local_height)
        within_tolerance = difference <= settings.BLOCK_HEIGHT_VARIANCE
    else:
        difference = -999
        within_tolerance = False

    # prepare response
    readyz_status = readyz_status and within_tolerance
    if within_tolerance:
        method_response_body += "[+] Node is within {} blocks of network\n".format(difference)
    else:
        method_response_body += (
            "[-] Node is outside tolerance and is {} blocks away from network\n".format(difference)
        )

    # return 200 if within tolerance or 503 if not
    if readyz_status:
        if verbose:
            return PlainTextResponse(method_response_body, 200)
        else:
            return PlainTextResponse("OK", 200)
    else:
        if verbose:
            return PlainTextResponse(method_response_body, 503)
        else:
            return PlainTextResponse("UNHEALTHY", 503)


@router.get("/healthz")
async def node_healthy(verbose: Optional[bool] = None):
    # empty response body for verbose responses
    method_response_body = ""

    # healthz response boolean that we'll bring along as we do our checks
    healthz_status = True

    # get local node's height
    local_height = get_icx_getLastBlock("http://localhost:9000/api/v3")

    # figure out if node response is appropriate
    if isinstance(local_height, type(None)):
        node_response = False
    else:
        node_response = True

    # handle node response
    healthz_status = healthz_status and node_response
    if node_response:
        method_response_body += "[+] Node is responsive"
    else:
        method_response_body += "[-] Node is NOT responsive"

    # return not 200 if not 200 or timeout
    if healthz_status:
        if verbose:
            return PlainTextResponse(method_response_body, 200)
        else:
            return PlainTextResponse("OK", 200)
    else:
        if verbose:
            return PlainTextResponse(method_response_body, 503)
        else:
            return PlainTextResponse("UNHEALTHY", 503)
