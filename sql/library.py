import sys
import json

from dataclasses import dataclass

from postgre import SqlServerResponses


@dataclass
class Customer:
    id: int
    first_name: str
    last_name: str


@dataclass
class Book:
    id: int
    name: str
    author: str
    present: int


class Library:
    def __init__(self, **kwargs):
        self._db = SqlServerResponses(**kwargs)

        self._books: list[Book] = []
        self._members: list[Customer] = []

        self._init_books()
        self._init_customers()

    def get_members(self):
        return [i.__dict__ for i in self._members]

    def find_book(self, book_name: str):
        for b in self._books:
            if b.name == book_name:
                return b
        return None

    def _find_book_id(self, id: int):
        for b in self._books:
            if b.id == id:
                return b
        return None

    def find_customer_name(self, first_name: str, last_name: str):
        for m in self._members:
            if m.first_name == first_name and m.last_name == last_name:
                return m
        return None

    def _find_customer_id(self, id: int):
        for m in self._members:
            if m.id == id:
                return m
        return None

    def _init_books(self):
        for book in self._db.select('*', 'books'):
            self._books.append(Book(*book))

    def _init_customers(self):
        for person in self._db.select('*', 'customer'):
            self._members.append(Customer(*person))

    def _check_in_db(self, person: Customer, book: Book) -> bool:
        if book and not self._find_book_id(book.id):
            print(f'Book {book.name} not found')
            return False
        if person and not self._find_customer_id(person.id):
            print(f'Customer {person.first_name} {person.last_name} not found')
            return False
        return True

    def create_new_customer(self, person: Customer):
        ans = self._db.select_where('*',
                                    'customer',
                                    ['first_name', 'last_name'],
                                    [person.first_name, person.last_name])
        if len(ans) != 0:  # такой человечек уже есть
            person.id = ans[0][0]
            return

        self._db.insert('customer', ['first_name', 'last_name'], [person.first_name, person.last_name])
        person.id = self._db.select_where('*',
                                          'customer',
                                          ['first_name', 'last_name'],
                                          [person.first_name, person.last_name])[0][0]
        self._members.append(person)

    def delete_customer(self, person: Customer):
        self._db.delete('customer', ['customer_id'], [person.id])

    def take_book(self, person: Customer, book: Book):

        if not self._find_book_id(book.id):
            print(f'Book {book.name} not found')
            return

        if book.present <= 0:  # no _books available
            print('book not available')
            return

        if not self._find_customer_id(person.id):
            self.create_new_customer(person)
            person.id = self._db.select_where('*',
                                              'customer',
                                              ['first_name', 'last_name'],
                                              [person.first_name, person.last_name])[0][0]

        date = '2021-08-01'
        self._db.insert('owned_books',
                        ['customer_id', 'book_id', 'return_date'],
                        [person.id, book.id, date])

        self._db.decrement('books', 'present', 'book_name', book.name)
        book.present -= 1
        return 1

    def return_book(self, person: Customer, book: Book):

        asn = self._db.select_where_owned_books(person.id, book.id)
        if len(asn) < 1:
            return  # no book taken

        self._db.return_book(person.id, book.id)
        self._db.increment('books', 'present', 'book_name', book.name)
        book.present += 1

    def print_owned_books(self):
        data = self._db.join_owned_books()
        keys = ['book_id', 'book_name', 'customer_id', 'return_date']
        d = [{key: value for key, value in zip(keys, i)} for i in data]
        return d


if __name__ == '__main__':
    with open("config.json", 'r') as f:
        d = json.load(f)

    lib = Library(**d)

    a = [i.__dict__ for i in lib._members]
    print(a)
    # c = Customer(None, "Ivan", "Ivanov")
    # lib.create_new_customer(c)
    #
    # lib.take_book(lib.find_customer_name("Ivan", "Ivanov"), lib.find_book('Sapiens'))
    # lib.take_book(lib.find_customer_name("Nikita", "Zalozhnyy"), lib.find_book('Crime and Punishment'))
    # lib.take_book(lib.find_customer_name("Ivan", "Ivanov"), lib.find_book('Crime and Punishment'))
    # lib.return_book(lib.find_customer_name("Ivan", "Ivanov"), lib.find_book('Sapiens'))
