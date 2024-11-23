from task import *
import pickle


# Декоратор для обработки ошибок
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "The arguments are not correct."
        except IndexError:
            return "The arguments are not correct."
        except TypeError:
            return "The arguments are not correct."
    return wrapper

# Парсинг ввода
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

# Функция для добавления контакта
@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)
    if not record:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added"
    else:
        record.add_phone(phone)
        return "Contact updated"
    
# Функция для изменения контакта
@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return "Contact updated"

# Функция для отображения телефона по имени
@input_error
def show_phone(args, book):
    name, *_ = args
    return f"\n{book.find(name)}\n"

# Функция для отображения всех контактов
@input_error
def show_all(book):
    if not book:
        return "No contacts found."
    return f"All contacts:\n {book}"

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    record.add_birthday(birthday)
    return "Contact updated"

@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    return f"{name}: {record.get_birthday()}"

@input_error
def birthdays(book):
    return book.get_upcoming_birthdays()

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def save_data(book, filename = "addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

# Основная функция
def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        match command:
            case "close" | "exit":
                print("Good bye!")
                break
            case "hello":
                print("How can I help you?")
            case "add":
                print(add_contact(args, book))
            case "change":
                print(change_contact(args, book))
            case "phone":
                print(show_phone(args, book))
            case "all":
                print(show_all(book))
            case "add-birthday":
                print(add_birthday(args, book))
            case "show-birthday":
                print(show_birthday(args, book))
            case "birthdays":
                print(birthdays(book))
            case _:
                print("Invalid command.")
    save_data(book)
if __name__ == "__main__":
    main()