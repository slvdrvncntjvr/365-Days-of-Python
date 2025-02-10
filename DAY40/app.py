import sys
from src.generator import QRCodeGenerator
from src.validators import validate_input
from pathlib import Path

def main():
    generator = QRCodeGenerator()
    
    while True:
        print("\nQR Code Generator")
        print("----------------")
        print("1. Generate QR Code")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1-2): ")
        
        if choice == "1":
            
            text = input("\nEnter the text for QR code: ")
            
            
            error = validate_input(text)
            if error:
                print(f"\nError: {error}")
                continue
            
            
            output_path = input("\nEnter output path (e.g., qr_codes/my_qr.png): ")
            
            try:
                
                result = generator.generate(text, output_path)
                print(f"\nQR code successfully generated at: {result}")
            except Exception as e:
                print(f"\nError: {str(e)}")
                
        elif choice == "2":
            print("\nGoodbye!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()