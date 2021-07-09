import sys
import psycopg2
import json


class SqlServerResponses:
    def __init__(self, database: str, user: str, password: str):
        self._database = database
        self._user = user
        self._password = password

        self._connection = self._init_connection()
        self._cursor = self._connection.cursor()

    def _init_connection(self):
        con = psycopg2.connect(
            database=self._database,
            user=self._user,
            password=self._password,
            host="127.0.0.1",
            port="5432"
        )
        return con

    def select(self, what: str, table_name: str):
        self._cursor.execute(f'SELECT {what} from {table_name};')
        return self._cursor.fetchall()

    def select_where(self, what: str, table_name: str, where_fields: list[str], where_values: list):
        statment = f'''SELECT {what} from {table_name}
         WHERE {self._format_where_response(where_fields, where_values)};'''
        self._cursor.execute(statment)
        return self._cursor.fetchall()

    def _format_where_response(self, where_fields: list[str], where_values: list) -> str:
        assert len(where_fields) == len(where_values)
        where_response = []
        where_response_str = ''

        for field, value in zip(where_fields, where_values):
            where_response.append(f"{field}='{value}'")

        if len(where_response) == 1:
            where_response_str = str(where_response[0])

        elif len(where_response) > 1:
            for i in range(len(where_response)):
                where_response_str += where_response[i]
                where_response_str += ' AND ' if i != len(where_response) - 1 else ''

        return where_response_str

    def _format_values(self, values: list[str]):
        values_out = []
        for i in range(len(values)):
            if type(values[i]) == str and values[i][0] == "\'" and values[i][-1] == "\'":
                values_out.append((values[i]))
            elif type(values[i]) == str:
                values_out.append(f"\'{values[i]}\'")
            else:
                values_out.append(str(values[i]))
        out_s = ""
        for i in values_out:
            out_s += i
        return ", ".join(values_out)

    def insert(self, table_name: str, fields: list[str], values: list[str]):
        assert len(fields) == len(values)

        statment = f'''INSERT INTO {table_name}({', '.join(fields)}) VALUES ({self._format_values(values)});'''
        self._cursor.execute(statment)
        self._connection.commit()

    def delete(self, table_name: str, fields: list, values: list):
        assert len(fields) == len(values)
        where = self._format_where_response(fields, values)
        statment = f'''DELETE FROM {table_name} WHERE {where};'''
        self._cursor.execute(statment)
        self._connection.commit()

    def increment(self, table_name: str, item: str, key: str, field_name: str):
        statment = f'''UPDATE {table_name} set {item} = {item} + 1 where {key} = '{field_name}';'''
        self._cursor.execute(statment)
        self._connection.commit()

    def decrement(self, table_name: str, item: str, key: str, field_name: str):
        statment = f'''UPDATE {table_name} set {item} = {item} - 1 where {key} = '{field_name}';'''
        self._cursor.execute(statment)
        self._connection.commit()

    def return_book(self, customer_id: int, book_id: int):
        statment = f'''DELETE FROM owned_books WHERE customer_id={customer_id} and book_id={book_id} ;'''
        self._cursor.execute(statment)
        self._connection.commit()

    def select_where_owned_books(self, customer_id: int, book_id: int):
        self._cursor.execute(f'SELECT * from owned_books WHERE customer_id={customer_id} and book_id={book_id};')
        return self._cursor.fetchall()

    def join_owned_books(self):

        statment = '''SELECT books.book_id, books.book_name, owned_books.customer_id, owned_books.return_date
                    FROM books INNER JOIN owned_books ON (owned_books.book_id = books.book_id);
                   '''
        self._cursor.execute(statment)
        return self._cursor.fetchall()


if __name__ == '__main__':
    with open("config.json", 'r') as f:
        d = json.load(f)

    ex = SqlServerResponses(**d)

    # print(ex.select_where('*', '123', ['a', 'b'], [1, 2]))
    print(ex.select('*', 'customer'))
