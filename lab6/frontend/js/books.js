var authors = [];
var lastAuthorId = 0;
var lastBookId = 0;

function loadAuthors() {
    url = "http://127.0.0.1:5000/get_all";
    console.log(url);
    $.get(url, function( data ) {
        console.log('Authors count: ' + data.length);
        authors = data;
        for (var i = 0; i < authors.length; i++) {
            if (authors[i].id > lastAuthorId) lastAuthorId = authors[i].id;
            for (var j = 0; j < authors[i].books.length; j++) {
                if (authors[i].books[j].id > lastBookId) lastBookId = authors[i].books[j].id;
            }
        }
        showAuthors();
    });
}

function saveData() {
    url = "http://127.0.0.1:5000/save_all";
    $.ajax(url, {
        data : JSON.stringify(authors),
        contentType : 'application/json',
        type : 'POST'});
}

function showAuthors() {
    html = "";
    for (var i = 0; i < authors.length; i++) {
        html += getAuthorHTML(authors[i]);
    }
    document.getElementById("authors-container").innerHTML = html;
    document.getElementById("back-button").style.display = "none";
    document.getElementById("add-author-button-div").style.display = "inline-block";
    document.getElementById("add-book-button-div").style.display = "none";
}

function clearModal() {
    document.getElementById('first-name').value = authors[j].firstname;
    document.getElementById('last-name').value = authors[j].lastname;
}

function showBooks(id) {
    for (var j = 0; j < authors.length; j++) {
        author = authors[j];
        if (author.id == id) {
            html = "";
            for (var i = 0; i < author.books.length; i++) {
                html += getBooksHTML(author, author.books[i]);
            }
            document.getElementById("authors-container").innerHTML = html;
            break;
        }
    }
    document.getElementById("back-button").style.display = "inline-block";
    document.getElementById("add-author-button-div").style.display = "none";
    document.getElementById("add-book-button-div").style.display = "inline-block";
    document.getElementById('modal-author-id').value = id;
}

function editAuthor(id) {
    if (id == 0) {
        document.getElementById('modal-author-id').value = 0;
        document.getElementById('modal-book-id').value = 0;
        document.getElementById('first-name').value = "";
        document.getElementById('last-name').value = "";
        document.getElementById('exampleModalLabel').innerHTML = "Author";
        document.getElementById('modal-first-name-label').value = "First name";
        document.getElementById('modal-last-name-label').value = "Last name";
        return;
    }
    for (var j = 0; j < authors.length; j++) {
        if (authors[j].id == id) {
            document.getElementById('modal-author-id').value = authors[j].id;
            document.getElementById('modal-book-id').value = 0;
            document.getElementById('first-name').value = authors[j].firstname;
            document.getElementById('last-name').value = authors[j].lastname;
            document.getElementById('exampleModalLabel').innerHTML = "Author";
            document.getElementById('modal-first-name-label').value = "First name";
            document.getElementById('modal-last-name-label').value = "Last name";
            break;
        }
    }
}

function editAuthorSave() {
    bookId = document.getElementById('modal-book-id').value;
    id = document.getElementById('modal-author-id').value;
    if (bookId != 0) {
        editBookSave(id, bookId);
        return;
    }
    if (id == 0) {
        lastAuthorId++;
        author = {
            "id": lastAuthorId,
            "firstname": document.getElementById('first-name').value,
            "lastname": document.getElementById('last-name').value,
            "books": []
        }
        authors.push(author);
        showAuthors();
        return;
    }
    for (var j = 0; j < authors.length; j++) {
        if (authors[j].id == id) {
            authors[j].firstname = document.getElementById('first-name').value;
            authors[j].lastname = document.getElementById('last-name').value;
            showAuthors();
            break;
        }
    }
}

function editBook(authorId, id) {
    if (id == 0) {
        //document.getElementById('modal-author-id').value = authorId;
        document.getElementById('modal-book-id').value = -1;
        document.getElementById('first-name').value = "";
        document.getElementById('last-name').value = "";
        document.getElementById('exampleModalLabel').innerHTML = "Book";
        document.getElementById('modal-first-name-label').innerHTML = "Title";
        document.getElementById('modal-last-name-label').innerHTML = "Year";
        return;
    }
    for (var j = 0; j < authors.length; j++) {
        if (authors[j].id == authorId) {
            for (var i = 0; i < authors[j].books.length; i++) {
                if (authors[j].books[i].id == id) {
                    book = authors[j].books[i];
                    //document.getElementById('modal-author-id').value = authorId;
                    document.getElementById('modal-book-id').value = book.id;
                    document.getElementById('first-name').value = book.title;
                    document.getElementById('last-name').value = book.year;
                    document.getElementById('exampleModalLabel').innerHTML = "Book";
                    document.getElementById('modal-first-name-label').innerHTML = "Title";
                    document.getElementById('modal-last-name-label').innerHTML = "Year";
                    break;
                }
            }
        }
    }
}

function editBookSave(authorId, id) {
    index = 0;
    for (var j = 0; j < authors.length; j++) {
        if (authors[j].id == authorId) {
            index = j;
            break;
        }
    }
    if (id == -1) {
        lastBookId ++;
        book = {
            "id": lastBookId,
            "title": document.getElementById('first-name').value,
            "year": document.getElementById('last-name').value,
            "author_id": authorId
        }
        authors[index].books.push(book);
        showBooks(authorId);
        return;
    }
    for (var j = 0; j < authors[index].books.length; j++) {
        if (authors[index].books[j].id == id) {
            authors[index].books[j].title = document.getElementById('first-name').value;
            authors[index].books[j].year = document.getElementById('last-name').value;
            showBooks(authorId);
            break;
        }
    }
}

function deleteAuthor(id) {
    for (var j = 0; j < authors.length; j++) {
        if (authors[j].id == id) {
            authors.splice(j, 1);
            showAuthors();
            break;
        }
    }
}

function deleteBook(authorId, id) {
    for (var j = 0; j < authors.length; j++) {
        if (authors[j].id == authorId) {
            for (var i = 0; i < authors[j].books.length; i++) {
                if (authors[j].books[i].id == id) {
                    authors[j].books.splice(i, 1);
                    showBooks(authorId);
                    break;
                }
            }
        }
    }
}

function getAuthorHTML(author) {
    var s = "";
    s += '<div class="card flex-row flex-wrap" style="margin-top: 20px;">';
    s += '<div class="card-block px-2 tour-content">';
    s += '<div class="tour-description-item">';
        s += '<svg style="width:24px;height:24px" viewBox="0 0 24 24">';
        s += '<path fill="#000000" d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z" /></svg>';
        s += '<span class="tour-description-item-text">' + author.firstname + ' ' + author.lastname + '</span>';
    s += '</div>';
    s += '<div class="tour-description-item">';
        s += '<svg style="width:24px;height:24px" viewBox="0 0 24 24">';
        s += '<path fill="#000000" d="M2,3H22C23.05,3 24,3.95 24,5V19C24,20.05 23.05,21 22,21H2C0.95,21 0,20.05 0,19V5C0,3.95 0.95,3 2,3M14,6V7H22V6H14M14,8V9H21.5L22,9V8H14M14,10V11H21V10H14M8,13.91C6,13.91 2,15 2,17V18H14V17C14,15 10,13.91 8,13.91M8,6A3,3 0 0,0 5,9A3,3 0 0,0 8,12A3,3 0 0,0 11,9A3,3 0   0,0 8,6Z" /></svg>';
        s += '<span class="tour-description-item-text">ID: ' + author.id + '</span>';
    s += '</div>';
    s += '</div>';
    s += '<div class="w-100"></div>';
        s += '<div class="align-middle card-footer w-100 text-muted">';
        s += '<div href="" class="btn btn-dark" style="float: right;" onclick="deleteAuthor(' + author.id + ')">Delete</div>';
        s += '<div href="" class="btn btn-dark" style="float: right; margin-right:10px;" onclick="editAuthor(' + author.id + ')" data-toggle="modal" data-target="#authorModal">Edit</div>';
        s += '<div href="" class="btn btn-dark" onclick="showBooks(' + author.id + ')">Show books</div>';
    s += '</div>';
    s += '</div>';
    return s;
}

function getBooksHTML(author, book) {
    var s = "";
    s += '<div class="card flex-row flex-wrap" style="margin-top: 20px;">';
    s += '<div class="card-block px-2 tour-content">';
    s += '<div class="tour-description-item">';
        s += '<svg style="width:24px;height:24px" viewBox="0 0 24 24">';
        s += '<path fill="#000000" d="M19,2L14,6.5V17.5L19,13V2M6.5,5C4.55,5 2.45,5.4 1,6.5V21.16C1,21.41 1.25,21.66 1.5,21.66C1.6,21.66 1.65,21.59 1.75,21.59C3.1,20.94 5.05,20.5 6.5,20.5C8.45,20.5 10.55,20.9 12,22C13.35,21.15 15.8,20.5 17.5,20.5C19.15,20.5 20.85,20.81 22.25,21.56C22.35,21.61 22.4,21.59 22.5,21.59C22.75,21.59 23,21.34 23,21.09V6.5C22.4,6.05 21.75,5.75 21,5.5V7.5L21,13V19C19.9,18.65 18.7,18.5 17.5,18.5C15.8,18.5 13.35,19.15 12,20V13L12,8.5V6.5C10.55,5.4 8.45,5 6.5,5V5Z" />';
        s += '<span class="tour-description-item-text">' + book.title + '</span>';
    s += '</div>';
    s += '<div class="tour-description-item">';
        s += '<svg style="width:24px;height:24px" viewBox="0 0 24 24">';
        s += '<path fill="#000000" d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z" /></svg>';
        s += '<span class="tour-description-item-text">' + author.firstname + ' ' + author.lastname + '</span>';
    s += '</div>';
    s += '<div class="tour-description-item">';
        s += '<svg style="width:24px;height:24px" viewBox="0 0 24 24">';
        s += ' <path fill="#000000" d="M19,19H5V8H19M16,1V3H8V1H6V3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3H18V1M17,12H12V17H17V12Z" />';
        s += '<span class="tour-description-item-text">' + book.year + '</span>';
    s += '</div>';
    s += '<div class="tour-description-item">';
        s += '<svg style="width:24px;height:24px" viewBox="0 0 24 24">';
        s += '<path fill="#000000" d="M13,12H20V13.5H13M13,9.5H20V11H13M13,14.5H20V16H13M21,4H3A2,2 0 0,0 1,6V19A2,2 0 0,0 3,21H21A2,2 0 0,0 23,19V6A2,2 0 0,0 21,4M21,19H12V6H21" />';
        s += '<span class="tour-description-item-text">ID: ' + book.id + '</span>';
    s += '</div>';
    s += '</div>';
    s += '<div class="w-100"></div>';
        s += '<div class="align-middle card-footer w-100 text-muted">';
        s += '<div href="" class="btn btn-dark" style="float: right;" onclick="deleteBook(' + author.id + ',' + book.id + ')">Delete</div>';
        s += '<div href="" class="btn btn-dark" style="float: right; margin-right:10px;" onclick="editBook(' + author.id + ',' + book.id + ')" data-toggle="modal" data-target="#authorModal">Edit</div>';
    s += '</div>';
    s += '</div>';
    return s;
}
