import pickle
from collections import UserDict
from datetime import datetime, timedelta
from dzshka import *


############################################################################################################

#                          dzshka.py- это название пайтон файла, если Вы не поняли)

############################################################################################################

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
###########################################################################
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
    except EOFError:
        return AddressBook()
############################################################################

def main():
    book = load_data()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip().lower()
        if not user_input:
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
            save_data(book)
        elif command == "add":
            print(add_contact(args, book))
            save_data(book)
        elif command == "change":
            print(change_phone(args, book))
            save_data(book)
        elif command == "phone":
            print(show_phone(args, book))
            save_data(book)
        elif command == "all":
            print(show_all(book))
            save_data(book)
        elif command == "add-birthday":
            print(add_birthday(args, book))
            save_data(book)
        elif command == "show-birthday":
            print(show_birthday(args, book))
            save_data(book)
        elif command == "birthdays":
            print(upcoming_birthdays(args if args else ["7"], book))
            save_data(book)
        else:
            print("Invalid command.")
            save_data(book)
    save_data(book)
if __name__ == "__main__":
    print(load_data())
    main()
#########
