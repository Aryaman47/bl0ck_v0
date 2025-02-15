from bl0ckchain.bl0ckchain import Blockchain
from bl0ckchain.display import display_chain, last_block

def main():
    blockchain = Blockchain()
    ddm_status = "❌"  # Initially, Dynamic Difficulty Mode (DDM) is OFF
     # Get the difficulty from the last block or set it to 1 if there are no blocks in the chain

    print("\nCurrent block(s) in the chain:")
    last_block(blockchain.chain)  # ✅ Pass the blockchain chain

    while True:
        Difficulty = blockchain.chain[-1].difficulty if blockchain.chain else 1 
        print(f"\n[ DDM {ddm_status} ] | Last Block Difficulty: {Difficulty}")  # Show DDM status
        print("\nOptions:")
        print("b - Create a new block")
        print("v - View blockchain")
        print("d - Enable Dynamic Difficulty Mode (Auto Mode by default)")
        print("r - Revert to Standard Mode (bl0ck v0)")
        print("n - Set manual difficulty (Only in DDM)")
        print("a - Switch back to Auto Mode (Only in DDM)")
        print("q - Quit")

        choice = input("\nEnter your choice: ").strip().lower()

        if choice == "b":
            blockchain.add_block()
            print("\nCurrent block(s) in the chain:")
            last_block(blockchain.chain)  # ✅ Pass blockchain.chain

        elif choice == "v":
            display_chain(blockchain.chain)  # ✅ Fix method call

        elif choice == "d":
            if blockchain.dynamic_difficulty_enabled:
                print("⚠️ DDM is already enabled!")  
            else:
                blockchain.enable_dynamic_difficulty()
                ddm_status = "✅"

        elif choice == "r":
            if not blockchain.dynamic_difficulty_enabled:
                print("⚠️ DDM is already in Standard Mode!")  
            else:
                blockchain.disable_dynamic_difficulty()
                ddm_status = "❌"
                print("🔄 Exiting to Standard Mode, DDM is disabled.")

        elif choice == "n":
            if blockchain.dynamic_difficulty_enabled:
                try:
                    difficulty = int(input("Enter difficulty (1-10): "))
                    blockchain.set_manual_difficulty(difficulty)
                except ValueError:
                    print("❌ Invalid input! Please enter a number between 1 and 10.")
            else:
                print("⚠️ Dynamic Difficulty Mode is not enabled! Press 'd' first.")

        elif choice == "a":
            if blockchain.dynamic_difficulty_enabled:
                blockchain.switch_to_auto_mode()
                print("🔄 Switched back to Auto Mode.")
            else:
                print("⚠️ Dynamic Difficulty Mode is not enabled!")

        elif choice == "q":
            print("Exiting...")
            break

        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()