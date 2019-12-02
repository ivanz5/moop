import db

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

db = db.DB()


def get_all():
    return db.get_authors_and_books()


def save_all(data):
    db.save_authors_and_books(data)


if __name__ == '__main__':
    server = SimpleJSONRPCServer(('localhost', 8080))
    server.register_function(get_all)
    server.register_function(save_all)
    server.serve_forever()
