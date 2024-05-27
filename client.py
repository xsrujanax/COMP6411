import socket
import os

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
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        choice = input(menu).strip()

        if choice == "1":
            first_name = input("Enter customer's first name:").strip().lower()
            request = f"FIND|{first_name}"

        elif choice == "2":
            first_name = input("Enter customer's first name: ").strip().lower()
            age = input("Enter customer's age: ").strip().lower()
            address = input("Enter customer's address: ").strip().lower()
            phone = input("Enter customer's phone: ").strip().lower()
            request = f"ADD|{first_name}|{age}|{address}|{phone}"
        
        elif choice == "3":
            first_name = input("Enter customer's first name: ").strip()
            request = f"DELETE|{first_name}"

        elif choice == "4":
            first_name = input("Enter customer's first name: ").strip()
            age = input("Enter new age: ").strip()
            request = f"UPDATE_AGE|{first_name}|{age}"
        
        elif choice == "5":
            first_name = input("Enter customer's first name: ").strip()
            address = input("Enter new address: ").strip()
            request = f"UPDATE_ADDRESS|{first_name}|{address}"

        elif choice == "6":
            first_name = input("Enter customer's first name: ").strip()
            phone = input("Enter new phone: ").strip()
            request = f"UPDATE_PHONE|{first_name}|{phone}"

        elif choice == "7":
            request = "PRINT|"

        elif choice == "8":
            print("Good bye")
            break

        else:
            print("Invalid option, please try again.")

        response = send_request(request)
        print(response)
        input("Press any key to continue...")

if __name__ == "__main__":
    main()

