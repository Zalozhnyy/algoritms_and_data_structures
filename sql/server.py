import json

from flask import Flask, abort, request, make_response, jsonify

from library import Library, Customer, Book

app = Flask(__name__)


@app.route('/api/customer/get_customers', methods=['GET'])
def get_customers():
    return jsonify(lib.get_members()), 200


@app.route('/api/customer/add_customers', methods=['POST'])
def post_test():
    assert 'first_name' in request.args
    assert 'last_name' in request.args
    d = {key: value for key, value in request.args.items()}
    c = Customer(None, d['first_name'], d['last_name'])
    lib.create_new_customer(c)
    return jsonify(c.__dict__), 201


@app.route('/api/customer/take_book', methods=['POST'])
def take_book():
    assert 'first_name' in request.args
    assert 'last_name' in request.args
    assert 'book_name' in request.args

    d = {key: value for key, value in request.args.items()}
    customer = lib.find_customer_name(d['first_name'], d['last_name'])
    book = lib.find_book(d['book_name'])
    if lib.take_book(customer, book):
        return f'Book {book.name} took by {customer.first_name} {customer.last_name}', 200
    else:
        return f'Book {book.name} cant be taken', 500


@app.route('/api/books/get_taken_books', methods=['GET'])
def get_taken_books():
    a = lib.print_owned_books()
    return jsonify(a), 200


if __name__ == '__main__':
    with open("config.json", 'r') as f:
        d = json.load(f)

    lib = Library(**d)

    app.run(debug=True)
