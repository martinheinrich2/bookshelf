"""
Module to get data of a book from its ISBN number via google books.
ISBN Number has to be a str!
"""
# %%
import urllib.request
import json
# to shorten the descripion we could import textwrapper


def main(isbn_input):
    """Get Book Data from Google Books

    Args:
        user_input (str): ISBN Number (10 or 13)

    Returns:
        book (list): title, subtitle, authors, publisher, pubDate, pages,
        isbn10, isbn13, description
    """
    book = []
    nobook = False
    user_input = str(isbn_input)
    google_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
    # Call URL with ISBN Number and read output
    with urllib.request.urlopen(google_api_link + user_input) as f:
        text = f.read()

        # important to set received data to utf-8
        decoded_text = text.decode("utf-8")
        # creates a dictionary from output. JSON format contains name/value pairs
        # the json.loads method parses the JSON string and converts it to a Python
        # dictionary
        meta_dict = json.loads(decoded_text)  # deserializing the JSON string
        # there are now tree keys (kind, totalItems, items) in the dictionary
        # book metadata is in items
    # insert try in case no book is found. Google returns only:
    # {"kind": "books#volumes","totalItems": 0}
    try:
        items_dict = meta_dict["items"][0]
    except KeyError:
        print('Book not found!')
        nobook = True

    # trying to end function if no book was found
    if nobook is True:
        book = []
        return book
    # info about the book is in volumeInfo
    volume_dict = items_dict["volumeInfo"]
    # %%
    title = volume_dict.get('title')
    subtitle = volume_dict.get('subtitle')
    authors1 = volume_dict.get('authors')
    authors = str(authors1)[2:-2]
    authors = authors.replace("', '", ", ")
    publisher = volume_dict.get('publisher')
    pubDate = volume_dict.get('publishedDate')
    pages = volume_dict.get('pageCount')
    description = volume_dict.get('description')
    isbnlist = volume_dict.get('industryIdentifiers')
    isbncodes = {elem.pop('type'): elem for elem in isbnlist}
    isbn10_id = isbncodes.get('ISBN_10')
    isbn13_id = isbncodes.get('ISBN_13')
    isbn10 = isbn10_id.get('identifier')
    isbn13 = isbn13_id.get('identifier')
    # collect relevant information about the book
    book = [title, subtitle, authors, publisher, pubDate, pages, isbn10, isbn13,
            description]
    return book


if __name__ == '__main__':
    main()
