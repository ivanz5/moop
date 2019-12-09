import pymysql
import os


class DB:
    def __init__(self):
        schema = os.environ.get('DB_SCHEMA', 'library')
        user = os.environ.get('DB_USER', 'user')
        password = os.environ.get('DB_PASSWORD', 'password')
        self.conn = pymysql.connect('localhost', user, password, schema)

    def save_authors_and_books(self, authors):
        with self.conn.cursor() as cur:
            cur.execute('DELETE FROM authors;')
            cur.execute('DELETE FROM books;')
            for author in authors:
                q = 'INSERT INTO authors(id, first_name, last_name) VALUES ({}, "{}", "{}");\n' \
                    .format(author['id'], author['firstname'], author['lastname'])
                cur.execute(q)
                for book in author['books']:
                    q = 'INSERT INTO books(id, title, year, author_id) VALUES ({}, "{}", {}, {});\n' \
                        .format(book['id'], book['title'], book['year'], book['author_id'])
                    cur.execute(q)
            self.conn.commit()

    def get_authors_and_books(self):
        with self.conn.cursor() as cur:
            cur.execute('SELECT id, first_name, last_name FROM authors')
            rows = cur.fetchall()
            res = list()
            for row in rows:
                author = {'id': row[0], 'firstname': row[1], 'lastname': row[2], 'books':[]}
                cur.execute('SELECT id, title, year FROM books WHERE author_id={}'.format(row[0]))
                books_rows = cur.fetchall()
                for book_row in books_rows:
                    author['books'].append({'id': book_row[0], 'title': book_row[1], 'year': int(book_row[2]), 'author_id': row[0]})
                res.append(author)
            return res
