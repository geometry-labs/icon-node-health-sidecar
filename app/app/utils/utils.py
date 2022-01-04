from .rpc import get_icx_getLastBlock


def get_top_block_height(peers: list) -> int:
    top_block_height = 0

    for p in peers[0:20]:
        block_height = get_icx_getLastBlock("http://" + p[0] + ":9000/api/v3")

        if isinstance(block_height, type(None)):
            block_height = 0

        if block_height > top_block_height:
            top_block_height = block_height

    return top_block_height
