import socketserver
import re
customers = {}

def add_customer(first_name, age, address, phone):
    customers[first_name] = {
        "age": age,
        "address" : address,
        "phone" : phone
    }

def get_customer_info(first_name):
    if first_name in customers:
        return customers[first_name]
    else:
        return f"No customer found with the name {first_name}"

def validate_record(record):
    details = record.split("|")
    if len(details) != 4:
        print("Record skipped [missing field(s)]:", record)
        return
    
    first_name = details[0].strip()
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

with open('data.txt','r') as file:
    for line in file:
        validate_record(line.strip())
    print(customers)
    print("Python DB server is now running...")