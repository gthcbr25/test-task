import json
import os

LIBRARY_FILE = 'library.json'


class Book:
    def __init__(self, id: int, title: str, author: str, year: str, status='в наличии'):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }


class Library:
    def __init__(self):
        self.books = self.load_library()
        self.next_id = self.generate_id()

    def load_library(self):  # Загрузка данных из json файла
        if os.path.exists(LIBRARY_FILE):
            with open(LIBRARY_FILE, 'r', encoding='utf-8') as file:
                return [Book(**book) for book in json.load(file)]
        return []

    def generate_id(self):  # генерация следующего id
        if self.books:
            return max(book.id for book in self.books) + 1
        return 1

    def save_library(self):  # Обновление данных в json файле
        with open(LIBRARY_FILE, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books], file, indent=4, ensure_ascii=False)

    def add_book(self, title: str, author: str, year: str):  # Добавление новой книги
        new_book = Book(self.next_id, title, author, year)
        self.next_id += 1
        self.books.append(new_book)  # Добавление книги в оперативную память
        self.save_library()  # Обновление json файла
        print("Книга успешно добавлена")

    def delete_book(self, book_id: int):  # Удаление книги по id
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_library()
                print("Книга успешно удалена")
                return
        print("Книга с таким ID не найдена")

    def search_books(self, search_type: str, search_value: str):  # Поиск книги по 1 параметру
        found_books = []
        translate = {
            'название': 'title',
            'автор': 'author',
            'год': 'year'
        }  # Перевод значения, которое ввел пользователь в нужный атрибут
        if search_type.lower() in translate:
            for book in self.books:
                if str(getattr(book, translate[search_type])).lower() == search_value.lower():
                    found_books.append(book)
        else:
            print('Неверный параметр поиска')
            return

        if found_books:
            for book in found_books:
                print(f"ID: {book.id},"
                      f" название: {book.title},"
                      f" автор: {book.author},"
                      f" год издания: {book.year},"
                      f" статус: {book.status}")
        else:
            print("Книги по указанному параметру не найдены")

    def display_books(self):  # Вывод всех сохраненных книг
        if self.books:
            for book in self.books:
                print(f"ID: {book.id},"
                      f" название: {book.title},"
                      f" автор: {book.author},"
                      f" год издания: {book.year},"
                      f" статус: {book.status}")
        else:
            print("Библиотека пуста")

    def change_status(self, book_id: int, new_status: str):  # Изменение статуса книги по id
        for book in self.books:
            if book.id == book_id:
                if new_status in ['в наличии', 'выдана']:
                    book.status = new_status
                    self.save_library()
                    print("Статус книги успешно изменен.")
                else:
                    print("Некорректный статус.")
                return
        print("Книга с таким ID не найдена.")


def main():
    library = Library()

    while True:
        print("\nВыберите действие:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Ваш выбор: ")

        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания книги: ")
            library.add_book(title, author, year)
        elif choice == '2':
            book_id = int(input("Введите ID книги для удаления: "))
            library.delete_book(book_id)
        elif choice == '3':
            search_type = input("Введите параметр поиска (название/автор/год): ").lower()
            search_value = input("Введите значение для поиска: ")
            library.search_books(search_type, search_value)
        elif choice == '4':
            library.display_books()
        elif choice == '5':
            book_id = int(input("Введите ID книги для изменения статуса: "))
            new_status = input("Введите новый статус (в наличии/выдана): ").lower()
            library.change_status(book_id, new_status)
        elif choice == '6':
            break
        else:
            print("Некорректный выбор. Пожалуйста, попробуйте снова")


if __name__ == '__main__':
    main()
