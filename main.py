from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        self._validate(value)
        super().__init__(value)
    def _validate(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must be exactly 10 digits")
        
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True
        raise ValueError("Old phone not found")
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        raise ValueError("Phone not found")
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        return f"{self.name.value}: {phones}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    def find(self, name):
        return self.data.get(name)
    def delete(self, name):
        if name in self.data:
            del self.data[name]                 
        



def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "This contact was not found."
        except IndexError:
            return "Please enter a valid command." 

    return inner


@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)
    if record:
        record.add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
    return "Contact added."

@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."
    

@input_error    
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError
    phones = "; ".join(p.value for p in record.phones)
    return f"{name}: {phones}"
   

def show_all(book):
    if not book.data:
        return "There are no contacts yet."
    
    result = []
    for record in book.data.values():
        result.append(str(record))
    return "\n".join(result)

@input_error
def delete_phone(args, book):
    name, phone = args
    record = book.find(name)
    if not record:
        raise KeyError
    record.remove_phone(phone)
    return "Phone removed."

@input_error
def delete_contact(args, book):
    name = args[0]
    book.delete(name)
    return "Contact deleted."    

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "delete":
            print(delete_contact(args, book))
        elif command == "remove-phone":
            print(delete_phone(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Джейн
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")
print(john)  # Ім'я контакту: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону в записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # John: 5555555555

# Видалення запису Jane
book.delete("Jane")