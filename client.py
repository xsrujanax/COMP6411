import socket
import os
import re

def send_request(request):
    HOST, PORT = "localhost", 9999
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(request.encode('utf-8'))

            response = sock.recv(1024).decode('utf-8')
            return response
    except ConnectionRefusedError:
        print(f"Failed to connect to the server at {HOST}:{PORT}")


def check_age(age):
    try:
        age = int(age)
        return 1<=age<=120
    except ValueError:
        return False
    
def check_phone(phone):
    phone_pattern = re.compile(r'^(\d{3} \d{3}-\d{4}|\d{3}-\d{4})$')
    return phone_pattern.match(phone) is not None

def check_address(address):
    address_pattern = re.compile(r'^[a-zA-Z0-9 .\-]+$')
    return address_pattern.match(address) is not None

def main():
    menu = """
Customer Management Menu
1. Find customer
2. Add customer
3. Delete customer
4. Update customer age
5. Update customer address
6. Update customer phone
7. Print report
8. Exit
Select: """
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        choice = input(menu).strip()

        if choice == "1":
            first_name = input("Enter customer's first name:").strip().lower()
            request = f"FIND|{first_name}"

        elif choice == "2":
            first_name = input("Enter customer's first name: ").strip().lower()

            age = input("Enter customer's age: ").strip().lower()
            while age and not check_age(age):
                print("Invalid age. Please enter a valid age between 1 and 120.")
                age = input("Enter customer's age: ").strip().lower()

            address = input("Enter customer's address: ").strip().lower()
            while address and not check_address(address):
                print("Invalid address. Please enter a valid address containing only alphanumeric characters, spaces, periods, and dashes.")
                address = input("Enter customer's address (optional): ").strip().lower()

            phone = input("Enter customer's phone: ").strip().lower()
            while phone and not check_phone(phone):
                print("Invalid phone number. Please enter a valid phone number (e.g., 123-4567 or 123 456-7890).")
                phone = input("Enter customer's phone: ").strip().lower()

            request = f"ADD|{first_name}|{age}|{address}|{phone}"
        
        elif choice == "3":
            first_name = input("Enter customer's first name: ").strip().lower()
            request = f"DELETE|{first_name}"

        elif choice == "4":
            first_name = input("Enter customer's first name: ").strip().lower()
            age = input("Enter new age: ").strip().lower()
            while age and not check_age(age):
                print("Age must be an integer (1 >= age <= 120). Please try again...")
                age = input("Enter customer's age: ").strip().lower()
            request = f"UPDATE_AGE|{first_name}|{age}"
        
        elif choice == "5":
            first_name = input("Enter customer's first name: ").strip().lower()
            address = input("Enter new address: ").strip().lower()
            while address and not check_address(address):
                print("Invalid address. Please enter a valid address containing only alphanumeric characters, spaces, periods, and dashes.")
                address = input("Enter customer's address: ").strip().lower()
            request = f"UPDATE_ADDRESS|{first_name}|{address}"

        elif choice == "6":
            first_name = input("Enter customer's first name: ").strip().lower()
            phone = input("Enter new phone: ").strip().lower()
            while phone and not check_phone(phone):
                print("Invalid phone number. Please enter a valid phone number (e.g., 123-4567 or 123 456-7890).")
                phone = input("Enter customer's phone: ").strip().lower()
            request = f"UPDATE_PHONE|{first_name}|{phone}"

        elif choice == "7":
            request = "PRINT|"

        elif choice == "8":
            print("Good bye")
            break

        else:
            print("Invalid option, please try again.")

        response = send_request(request)
        print("Server response:", response)
        input("Press any key to continue...")

if __name__ == "__main__":
    main()

