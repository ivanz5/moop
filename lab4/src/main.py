import wx
import xmltodict
import json
import db
import requests
from jsonrpclib import Server


conn = Server('http://localhost:8080')


class Dialog(wx.Dialog):
    def __init__(self, parent, title):
        super().__init__(parent=parent, title=title)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_sizer)

    def add_widgets(self, label_text, text_ctrl):
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, label=label_text,size=(50, -1))
        row_sizer.Add(label, 0, wx.ALL, 5)
        row_sizer.Add(text_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        self.main_sizer.Add(row_sizer, 0, wx.EXPAND)


class AuthorDialog(Dialog):
    def __init__(self, author):
        super().__init__(parent=None, title='Author')
        self.author = author
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.first_name = wx.TextCtrl(self, value=author['firstname'])
        self.last_name = wx.TextCtrl(self, value=author['lastname'])
        self.add_widgets('First name', self.first_name)
        self.add_widgets('Last name', self.last_name)
        btn_sizer = wx.BoxSizer()
        save_btn = wx.Button(self, label='Save')
        save_btn.Bind(wx.EVT_BUTTON, self.on_save)
        btn_sizer.Add(save_btn, 0, wx.ALL, 5)
        btn_sizer.Add(wx.Button(self, id=wx.ID_CANCEL), 0, wx.ALL, 5)
        self.main_sizer.Add(btn_sizer, 0, wx.CENTER)
        self.SetSizer(self.main_sizer)

    def on_save(self, event):
        self.author['firstname'] = self.first_name.GetValue()
        self.author['lastname'] = self.last_name.GetValue()
        self.Close()


class BookDialog(Dialog):
    def __init__(self, book):
        super().__init__(parent=None, title='Book')
        self.book = book
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.title = wx.TextCtrl(self, value=book['title'])
        self.year = wx.TextCtrl(self, value=book['year'])
        self.add_widgets('Title', self.title)
        self.add_widgets('Year', self.year)
        btn_sizer = wx.BoxSizer()
        save_btn = wx.Button(self, label='Save')
        save_btn.Bind(wx.EVT_BUTTON, self.on_save)
        btn_sizer.Add(save_btn, 0, wx.ALL, 5)
        btn_sizer.Add(wx.Button(self, id=wx.ID_CANCEL), 0, wx.ALL, 5)
        self.main_sizer.Add(btn_sizer, 0, wx.CENTER)
        self.SetSizer(self.main_sizer)

    def on_save(self, event):
        self.book['title'] = self.title.GetValue()
        self.book['year'] = self.year.GetValue()
        self.Close()


class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_author_index = -1
        self.selected_book_index = -1
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.last_author_id = 0
        self.last_book_id = 0

        # Authors list
        self.list_ctrl = wx.ListCtrl(
            self, size=(-1, 100),
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.list_ctrl.InsertColumn(0, 'ID', width=50)
        self.list_ctrl.InsertColumn(1, 'First name', width=140)
        self.list_ctrl.InsertColumn(2, 'Last name', width=140)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_author_selected)
        main_sizer.Add(self.list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        # Books list
        self.books_ctrl = wx.ListCtrl(
            self, size=(-1, 150),
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        # self.books_ctrl.InsertColumn(0, 'ID', width=50)
        self.books_ctrl.InsertColumn(0, 'Title', width=140)
        self.books_ctrl.InsertColumn(1, 'Year', width=140)
        self.books_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_book_selected)
        main_sizer.Add(self.books_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        # Buttons
        self.load_button = wx.Button(self, label='Load')
        self.load_button.Bind(wx.EVT_BUTTON, self.on_load_data)
        main_sizer.Add(self.load_button, 0, wx.ALL | wx.CENTER, 5)
        self.save_button = wx.Button(self, label='Save')
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save_data)
        main_sizer.Add(self.save_button, 0, wx.ALL | wx.CENTER, 5)
        self.edit_button = wx.Button(self, label='Edit selected')
        self.edit_button.Bind(wx.EVT_BUTTON, self.on_edit_selected)
        main_sizer.Add(self.edit_button, 0, wx.ALL | wx.CENTER, 5)
        self.delete_button = wx.Button(self, label='Delete selected')
        self.delete_button.Bind(wx.EVT_BUTTON, self.on_delete_selected)
        main_sizer.Add(self.delete_button, 0, wx.ALL | wx.CENTER, 5)
        self.create_author_button = wx.Button(self, label='Create author')
        self.create_author_button.Bind(wx.EVT_BUTTON, self.on_create_author)
        main_sizer.Add(self.create_author_button, 0, wx.ALL | wx.CENTER, 5)
        self.create_book_button = wx.Button(self, label='Create book')
        self.create_book_button.Bind(wx.EVT_BUTTON, self.on_create_book)
        main_sizer.Add(self.create_book_button, 0, wx.ALL | wx.CENTER, 5)

        self.SetSizer(main_sizer)
        # Database
        self.db = db.DB()

    def on_load_data(self, event):
        self.selected_author_index = -1
        self.selected_book_index = -1
        # resp = requests.get('http://127.0.0.1:5000/get_all')
        self.authors = conn.get_all()
        # Set last ids
        for author in self.authors:
            if author['id'] > self.last_author_id:
                self.last_author_id = author['id']
            for book in author['books']:
                if book['id'] > self.last_book_id:
                    self.last_book_id = book['id']
        self.on_load_data_show()

    def on_save_data(self, event):
        # requests.post('http://127.0.0.1:5000/save_all', json=self.authors)
        conn.save_all(self.authors)

    def on_load_data_show(self):
        # Show authors list
        self.list_ctrl.ClearAll()
        self.list_ctrl.InsertColumn(0, 'ID', width=50)
        self.list_ctrl.InsertColumn(1, 'First name', width=140)
        self.list_ctrl.InsertColumn(2, 'Last name', width=140)
        # print(json.dumps(untangle.parse('data.xml'), indent=4))
        index = 0
        for author in self.get_authors():
            self.list_ctrl.InsertItem(index, str(author['id']))
            self.list_ctrl.SetItem(index, 1, author['firstname'])
            self.list_ctrl.SetItem(index, 2, author['lastname'])
            index += 1
        # Show books if author selected
        if self.selected_author_index >= 0:
            self.on_author_selected(None)

    def on_edit_selected(self, event):
        # Edit book if selected
        if self.selected_book_index >= 0:
            book = self.get_books(self.get_authors()[self.selected_author_index])[self.selected_book_index]
            dialog = BookDialog(book)
            dialog.ShowModal()
            dialog.Destroy()
            self.on_load_data_show()
        # Edit author is selected
        elif self.selected_author_index >= 0:
            author = self.get_authors()[self.selected_author_index]
            dialog = AuthorDialog(author)
            dialog.ShowModal()
            dialog.Destroy()
            self.on_load_data_show()

    def on_delete_selected(self, event):
        # Delete book if selected
        if self.selected_book_index >= 0:
            book = self.get_books(self.get_authors()[self.selected_author_index])[self.selected_book_index]
            self.authors[self.selected_author_index]['books'].remove(book)
            self.on_load_data_show()
        # Delete author if selected
        elif self.selected_author_index >= 0:
            author = self.get_authors()[self.selected_author_index]
            self.authors.remove(author)
            self.on_load_data_show()
            self.selected_author_index = -1
            self.selected_book_index = -1
            self.books_ctrl.ClearAll()

    def on_create_author(self, event):
        author = {'firstname': '', 'lastname': ''}
        dialog = AuthorDialog(author)
        dialog.ShowModal()
        dialog.Destroy()
        if author['firstname'] == '' or author['lastname'] == '':
            return None
        author['id'] = self.next_author_id()
        author['books'] = []
        self.authors.append(author)
        self.selected_author_index = -1
        self.selected_book_index = -1
        self.on_load_data_show()

    def on_create_book(self, event):
        if self.selected_author_index < 0:
            return None
        book = {'title': '', 'year': ''}
        dialog = BookDialog(book)
        dialog.ShowModal()
        dialog.Destroy()
        if book['title'] == '' or book['year'] == '':
            return None
        book['id'] = self.next_book_id()
        book['author_id'] = self.get_authors()[self.selected_author_index]['id']
        # print(book)
        books = self.get_books(self.get_authors()[self.selected_author_index])
        books.append(book)
        # self.selected_author_index = -1
        self.selected_book_index = -1
        self.on_load_data_show()

    def on_author_selected(self, event):
        # Load author's books
        if event is not None:
            self.selected_author_index = event.Index
        if self.selected_author_index < 0:
            return None
        self.selected_book_index = -1
        self.books_ctrl.ClearAll()
        # self.books_ctrl.InsertColumn(0, 'ID', width=50)
        self.books_ctrl.InsertColumn(0, 'Id', width=140)
        self.books_ctrl.InsertColumn(1, 'Title', width=140)
        self.books_ctrl.InsertColumn(2, 'Year', width=140)
        author = self.get_authors()[self.selected_author_index]
        books = self.get_books(author)
        index = 0
        for book in books:
            self.books_ctrl.InsertItem(index, str(book['id']))
            self.books_ctrl.SetItem(index, 1, book['title'])
            self.books_ctrl.SetItem(index, 2, str(book['year']))
            index += 1

    def on_book_selected(self, event):
        self.selected_book_index = event.Index

    def get_authors(self):
        return self.authors

    def get_books(self, author):
        if author.get('books') is None:
            author['books'] = []
        return author['books']

    def next_author_id(self, increment=True):
        if increment:
            self.last_author_id = self.last_author_id + 1
        return self.last_author_id

    def next_book_id(self, increment=True):
        if increment:
            self.last_book_id = self.last_book_id + 1
        return self.last_book_id


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Lab 1. XML', size=(350, 550))
        self.panel = MainPanel(self)
        self.Show()

if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()

