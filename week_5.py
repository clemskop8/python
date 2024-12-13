import json

class Book:
    def __init__(self, title, author, year, genre):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

    def __str__(self):
        return f"'{self.title}' {self.author}, {self.year} ({self.genre})"

    def __eq__(self, other):
        if isinstance(other, Book):
            return self.title == other.title and self.author == other.author
        return False


class Reader:
    def __init__(self, name, reader_id):
        self.name = name
        self.reader_id = reader_id
        self.borrowed_books = []

    def borrow_book(self, book):
        if book not in self.borrowed_books:
            self.borrowed_books.append(book)
        else:
            raise Exception(f"Книга '{book.title}' уже взята этим читателем.")

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
        else:
            raise Exception(f"Книга '{book.title}' не была взята этим читателем.")

    def __str__(self):
        return f"Читатель {self.name} (ID: {self.reader_id})"

    def get_borrowed_books(self):
        return [str(book) for book in self.borrowed_books]


class Library:
    def __init__(self, name):
        self.name = name
        self.books = []
        self.readers = []

    def add_book(self, book):
        if book not in self.books:
            self.books.append(book)
        else:
            raise Exception(f"Книга '{book.title}' уже добавлена в библиотеку.")

    def remove_book(self, book):
        if book in self.books:
            self.books.remove(book)
        else:
            raise Exception(f"Книга '{book.title}' не найдена в библиотеке.")

    def register_reader(self, reader):
        if reader not in self.readers:
            self.readers.append(reader)
        else:
            raise Exception(f"Читатель {reader.name} уже зарегистрирован.")

    def lend_book(self, reader, book):
        if book not in self.books:
            raise Exception(f"Книга '{book.title}' не найдена в библиотеке.")
        if book in reader.borrowed_books:
            raise Exception(f"Читатель {reader.name} уже взял эту книгу.")
        reader.borrow_book(book)
        self.books.remove(book)

    def return_book(self, reader, book):
        if book not in reader.borrowed_books:
            raise Exception(f"Читатель {reader.name} не взял эту книгу.")
        reader.return_book(book)
        self.books.append(book)

    def find_book(self, title=None, author=None):
        found_books = []
        for book in self.books:
            if title and title.lower() in book.title.lower():
                found_books.append(book)
            if author and author.lower() in book.author.lower():
                found_books.append(book)
        return found_books

    def get_reader_books(self, reader):
        return reader.get_borrowed_books()

    def save_to_file(self, filename):
        data = {
            'books': [book.__dict__ for book in self.books],
            'readers': [{
                'name': reader.name,
                'reader_id': reader.reader_id,
                'borrowed_books': [book.__dict__ for book in reader.borrowed_books]
            } for reader in self.readers]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.books = [Book(**book_data) for book_data in data['books']]
            self.readers = []
            for reader_data in data['readers']:
                reader = Reader(reader_data['name'], reader_data['reader_id'])
                for book_data in reader_data['borrowed_books']:
                    reader.borrow_book(Book(**book_data))
                self.readers.append(reader)
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
        except json.JSONDecodeError:
            print(f"Ошибка при чтении файла {filename}.")


library = Library("Центральная библиотека")

book1 = Book("1984", "Джордж Оруэлл", 1949, "Дистопия")
book2 = Book("Мастер и Маргарита", "Михаил Булгаков", 1966, "Роман")

library.add_book(book1)
library.add_book(book2)

reader1 = Reader("Иван Иванов", 1)
reader2 = Reader("Мария Петрова", 2)

library.register_reader(reader1)
library.register_reader(reader2)

library.lend_book(reader1, book1)

print(f"{reader1.name} взял книги: {reader1.get_borrowed_books()}")

library.save_to_file('library.json')

new_library = Library("Новая библиотека")
new_library.load_from_file('library.json')
print(f"Загруженные книги: {[str(book) for book in new_library.books]}")
