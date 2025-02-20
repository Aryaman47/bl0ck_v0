def display_chain(chain):
    """Return the entire blockchain as a list of dictionaries."""
    if not chain:
        return []  # Return an empty list if the blockchain has no blocks

    return [
        {
            "index": block.index,
            "timestamp": block.timestamp,
            "mining_time": block.mining_time,
            "data": block.data,
            "difficulty": block.difficulty,
            "previous_hash": block.previous_hash,
            "hash": block.hash
        }
        for block in chain
    ]


def last_block(chain):
    """Return the last block as a dictionary."""
    if not chain:
        return None  # Return None if the blockchain is empty

    block = chain[-1]
    return {
        "index": block.index,
        "timestamp": block.timestamp,
        "mining_time": block.mining_time,
        "data": block.data,
        "difficulty": block.difficulty,
        "previous_hash": block.previous_hash,
        "hash": block.hash
    }
