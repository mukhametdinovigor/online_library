import json
import urllib.parse
import math
import os
import more_itertools

from environs import Env
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def get_books(book_json_path, books_per_page):
    with open(book_json_path, 'r', encoding='utf-8') as file:
        books_json = file.read()
    books = json.loads(books_json)
    pages_count = math.ceil(len(books) / books_per_page)
    for book in books:
        book['book_path'] = urllib.parse.quote(book.get('book_path'))
        book['img_src'] = urllib.parse.quote(book.get('img_src'))
    chunked_books = list(more_itertools.chunked(books, books_per_page))
    return pages_count, chunked_books


def render_page(template, pages_count, page_number, first_col_books, second_col_books, folder):
    rendered_page = template.render(
        folder=folder,
        pages_count=pages_count,
        page_number=page_number,
        first_col_books=first_col_books,
        second_col_books=second_col_books
    )
    with open(os.path.join(folder, f'index{page_number}.html'), 'w', encoding="utf8") as file:
        file.write(rendered_page)


def on_reload():
    env = Env()
    env.read_env()
    folder = env('FOLDER', default='pages')
    books_per_page = int(env('BOOKS_PER_PAGE', default=10))
    books_per_col = int(books_per_page / 2)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    pages_count, chunked_books = get_books('books.json', books_per_page)
    os.makedirs(folder, exist_ok=True)
    for page_number, books_on_page in enumerate(chunked_books, 1):
        if len(books_on_page) > books_per_col:
            first_col_books, second_col_books = more_itertools.chunked(books_on_page, books_per_col)
            render_page(template, pages_count, page_number, first_col_books, second_col_books, folder)
        else:
            first_col_books = books_on_page
            second_col_books = []
            render_page(template, pages_count, page_number, first_col_books, second_col_books, folder)


if __name__ == '__main__':
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', default_filename='pages/index1.html')
