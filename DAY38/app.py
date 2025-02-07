import json
from blockchain import Blockchain
import sys

def print_menu():
    print("\n=== Simple Blockchain Simulator ===")
    print("1. Add a new transaction")
    print("2. Mine a new block")
    print("3. Display the blockchain")
    print("4. Check blockchain validity")
    print("5. Exit")

def main():
    blockchain = Blockchain(difficulty=3)
    
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            sender = input("Sender: ").strip()
            receiver = input("Receiver: ").strip()
            amount = input("Amount: ").strip()
            transaction = {"sender": sender, "receiver": receiver, "amount": amount}
            blockchain.add_new_transaction(transaction)
            print("Transaction added!")
        elif choice == "2":
            print("Mining new block... This might take a few moments.")
            new_block = blockchain.mine()
            if new_block:
                print("Block mined successfully!")
                print("Block hash:", new_block.hash)
            else:
                print("No transactions to mine.")
        elif choice == "3":
            chain = blockchain.to_dict()
            print("\nBlockchain:")
            print(json.dumps(chain, indent=4, sort_keys=True))
        elif choice == "4":
            if blockchain.is_chain_valid():
                print("The blockchain is valid.")
            else:
                print("The blockchain is invalid!")
        elif choice == "5":
            print("Exiting... Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
