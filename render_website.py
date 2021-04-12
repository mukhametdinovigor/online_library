import json
import math
import os
import more_itertools

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from werkzeug.urls import url_fix


def get_books(book_json_path, books_per_page):
    with open(book_json_path, 'r', encoding='utf-8') as file:
        books_json = file.read()
    books = json.loads(books_json)
    pages_count = math.ceil(len(books) / books_per_page)
    for book in books:
        book['book_path'] = url_fix(book.get('book_path'))
        book['img_src'] = url_fix(book.get('img_src'))
    chunked_books = list(more_itertools.chunked(books, books_per_page))
    return pages_count, chunked_books


def on_reload():
    folder = 'docs'
    books_per_page = 10
    books_per_col = int(books_per_page / 2)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    pages_count, chunked_books = get_books('books.json', books_per_page)
    os.makedirs(folder, exist_ok=True)
    for page_number, book in enumerate(chunked_books, 1):
        if len(book) > books_per_col:
            first_col_books, second_col_books = more_itertools.chunked(book, books_per_col)

            rendered_page = template.render(
                pages_count=pages_count,
                page_number=page_number,
                first_col_books=first_col_books,
                second_col_books=second_col_books
            )
            with open(os.path.join(folder, f'index{page_number}.html'), 'w', encoding="utf8") as file:
                file.write(rendered_page)
        else:
            first_col_books = book
            rendered_page = template.render(
                pages_count=pages_count,
                page_number=page_number,
                first_col_books=first_col_books,
            )
            with open(os.path.join(folder, f'index{page_number}.html'), 'w', encoding="utf8") as file:
                file.write(rendered_page)


if __name__ == '__main__':
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='docs', default_filename='index.html')
