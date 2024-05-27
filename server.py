import socketserver
import re
import os

customers = {}

def add_customer(first_name, age, address, phone):
    if first_name.lower() in customers:
            return f"Customer {first_name} already exists"
    customers[first_name] = {
        "age": age,
        "address" : address,
        "phone" : phone
    }
    return f"Customer {first_name} added successfully"

def get_customer_info(first_name):
    customer = customers.get(first_name.lower())
    if first_name in customers:
        return f"{first_name}|{customer['age']}|{customer['address']}|{customer['phone']}"
    else:
        return f"No customer found with the name {first_name}"

def validate_record(record):
    details = record.split("|")
    if len(details) != 4:
        print("Record skipped [missing field(s)]:", record)
        return
    
    first_name = details[0].strip().lower()
    age = details[1].strip()
    address = details[2].strip()
    phone = details[3].strip()
    
    if not first_name:
        print("Record skipped [missing first name]:", record)
        return
    
    if age:
        age = int(age)
        if not (1 <= age <=120):
            print("Record skipped [invalid age field]:", record)
            return
    
    if address:
        if not re.match(r'^[a-zA-Z0-9 .\-]+$',address):
            print("Record skipped [invalid address field]:", record)
            return

    if phone:
        phone_pattern = re.compile(r'^(\d{3} \d{3}-\d{4}|\d{3}-\d{4})$')
        if not phone_pattern.match(phone):
            print("Record skipped [invalid phone field]:", record)
            return

    add_customer(first_name,age,address,phone)

def load_data():
    with open('data.txt','r') as file:
        for line in file:
            validate_record(line.strip())
        print(customers)
        print("Python DB server is now running...")

class DBSever(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            self.data = self.request.recv(1024).strip()
            command, * params = self.data.decode('utf-8').split("|")

            if command == "FIND":
                response = get_customer_info(params[0])
            
            elif command == "ADD":
                response = add_customer(params[0],params[1],params[2],params[3])
            else:
                response = "Invalid command"

            self.request.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"Exception occurred: {e}")

if __name__ == "__main__":
    load_data()
    HOST, PORT = "localhost", 9999
    with socketserver.TCPServer((HOST, PORT), DBSever) as server:
        print("Server started at {}:{}".format(HOST, PORT))
        server.serve_forever()