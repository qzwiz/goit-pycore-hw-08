from collections import UserDict
from datetime import datetime
import re
from datetime import date, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
		pass

class Birthday(Field):
    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError("Date must be a string in the format DD.MM.YYYY")
        try: datetime.strptime(value, "%d.%m.%Y")            
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        self.value = value 
 
class Phone(Field):
    def __init__(self, value):
           if not (len(value) == 10 and value.isdigit()):
               raise ValueError("нужно 10 цифр")
           super().__init__(value)
            

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)
    
    def edit_phone(self, old_phone, new_phone):
        phone_obj = self.find_phone(old_phone)
        if not phone_obj:
            raise ValueError("Phone number not found.")
        self.add_phone(new_phone)
        self.remove_phone(old_phone)

        

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        details = [f"Contact name: {self.name.value}"]
        if self.phones:
            details.append(f"Phones: {', '.join(p.value for p in self.phones)}")
        if self.birthday:
            details.append(f"Birthday: {self.birthday.value}")
        return "; ".join(details)

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        

    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = datetime.today().date()

        for record in self.data.values():
            if not record.birthday:
                continue

            birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            birthday_this_year = birthday_date.replace(year=today.year)


            if birthday_this_year < today:
                birthday_this_year = record.birthday.value.replace(year=today.year + 1)

            adjusted_birthday = self.adjust_for_weekend(birthday_this_year)

            if 0 <= (adjusted_birthday - today).days <= days:
                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": adjusted_birthday.strftime("%d-%m-%Y")
                })

        return upcoming_birthdays
    @staticmethod
    def adjust_for_weekend(date):
            if date.weekday() == 5:  # Субота
                return date + timedelta(days=2)
            elif date.weekday() == 6:  # Неділя
                return date + timedelta(days=1)
            return date 

    def find(self, name):
        return self.data.get(name, None)
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
    
    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
    

#############<<<<<<<<<

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Не вірний формат вводу."
        except IndexError:
            return "Контакт не знайдено."

    return inner


############>>>>>>>>>>>
    
@input_error
def add_contact(args, book):
    if len(args) < 2:
        return "Usage: add [name] [phone]"
    name, phone = args
    if name in book.data:
        book.data[name].add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
    return f"Added {name} with phone {phone}"

@input_error
def change_phone(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"Updated {name}'s phone from {old_phone} to {new_phone}"
    return "Contact not found."

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return f"{name}: {', '.join(p.value for p in record.phones)}"
    return "Contact not found."

@input_error
def show_all(book):
    if not book.data:
        return "Address book is empty."
    result = []
    for name, record in book.data.items():
        result.append(str(record))

    return "\n".join(result)

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Added birthday {birthday} for {name}"
    return "Contact not found."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday.value}"
    return "Birthday not found for this contact."


@input_error
def upcoming_birthdays(args, book):
    days = int(args[0]) if args else 7
    upcoming_birthdays = book.get_upcoming_birthdays(days)
    return "\n".join(f"{b['name']}: {b['congratulation_date']}" for b in upcoming_birthdays)
    



def parse_input(user_input):
    return user_input.strip().split()


print('РАБОТАЕМ?)))) 🥶')

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip().lower()
        if not user_input:
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_phone(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(upcoming_birthdays(args if args else ["7"], book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

