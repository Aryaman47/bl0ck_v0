from bl0ck import Blockchain

def main():
    blockchain = Blockchain()
    blockchain.display_chain()

    while True:
        print("\nOptions:")
        print("b - Create a new block")
        print("v - View blockchain")
        print("d - Enable Dynamic Difficulty Mode")
        print("r - Revert to Standard Mode (bl0ck v0)")
        print("q - Quit")

        choice = input("\nEnter your choice: ").lower()

        if choice == "b":
            blockchain.add_block()
        elif choice == "v":
            blockchain.display_chain()
        elif choice == "d":
            blockchain.enable_dynamic_difficulty()
        elif choice == "r":
            blockchain.disable_dynamic_difficulty()
        elif choice == "q":
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
