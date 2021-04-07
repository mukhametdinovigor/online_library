import json
import math
import more_itertools

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from werkzeug.urls import url_fix


def get_books(book_json_path):
    with open(book_json_path, 'r', encoding='utf-8') as file:
        books_json = file.read()
    books = json.loads(books_json)
    for book in books:
        book['book_path'] = url_fix(book.get('book_path'))
    first_col_books, second_col_books = more_itertools.chunked(books, math.ceil(len(books) / 2))
    return first_col_books, second_col_books


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    first_col_books, second_col_books = get_books('books.json')
    rendered_page = template.render(
        first_col_books=first_col_books,
        second_col_books=second_col_books
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


if __name__ == '__main__':
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')

