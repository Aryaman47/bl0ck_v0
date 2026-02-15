# backend/bl0ckchain/storage.py
import json
import os
from .bl0ck import Block

FILE_NAME = "blockchain_data.json"

def save_to_file(chain):
    with open(FILE_NAME, "w") as file:
        json.dump([block.__dict__ for block in chain], file, indent=4)

def load_from_file():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            try:
                data = json.load(file)
                if data:
                    return [
                        Block(
                            block["index"],
                            block["timestamp"],
                            block["data"],
                            block["previous_hash"],
                            block.get("difficulty", 1),
                            block.get("nonce", 0),
                            block.get("mining_time", None)
                        )
                        for block in data
                    ]
            except json.JSONDecodeError:
                pass
    return []
