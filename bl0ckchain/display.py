
def display_chain(chain):
    print("\n🔗 Blockchain Data:")
    for block in chain:
        print(f"\nIndex: {block.index} | Time: {block.mining_time}s")
        print(f"Timestamp: {block.timestamp}")
        print(f"Data: {block.data}")
        print(f"Difficulty: {block.difficulty}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Hash: {block.hash}")
        print("-" * 40)

def last_block(chain):
    block = chain[-1]
    print(f"\nIndex: {block.index} | Time: {block.mining_time}s")
    print(f"Timestamp: {block.timestamp}")
    print(f"Data: {block.data}")
    print(f"Difficulty: {block.difficulty}")
    print(f"Previous Hash: {block.previous_hash}") 
    print(f"Hash: {block.hash}")
