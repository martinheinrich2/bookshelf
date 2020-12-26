## Bookshelf

This is the result of an exercise to explore computer-vision and python.
There are several tutorials about reading and decoding barcode using OpenCV
and pyzbar.

The program can read a barcode from a book, get information about the book
from Google Books, store the information in a Sqlite3 database, add books
manually, search the database, delete entries and export data to a csv-file.

The following modules are imported into the main program:

# scan_barcodes.py is a module that captures video from the webcam, decodes
barcodes/QR codes and writes them to barcodes.csv. It relies on open-cv,
pyzbar/zbar modules.

# get_isbn_meta.py is a module to look up ISBN Codes using Google Api,
it takes an ISBN number as argument, that has to be a string!

# db_handler.py is a class to interact with the Sqlite3 database.

# bookshelf.py is the main library program
It imports scan_barcodes.py, get_isbn_code.py and db_handler.py.

Programm functions:

1. Scan Barcodes: Uses open-cv and pyzbar to scan barcodes from webcam frames.
   It writes barcodes to a csv file with name barcodes + timestamp.

2. Get Book data from Google: Opens a filedialog to read a barcodes-xxxx.csv
   file. Then it uses the Google api at:
   https://www.googleapis.com/books/v1/volumes?q=isbn:
   and gets book metadata from Google Books. It writes the book data to a file:
   "book_data.csv".

3. View Books: Load book_library.db and display information about books.

4. Search Title/Author: Works partially, needs some improvement!

5. Add Book: Add book to database, except for a description!

6. Update Entry: Allows to modify the information about a book.

7. Delete Book: Deletes a chosen book from the database.

8. Create Database: Creates an empty Sqlite3 database if none exists, with
   name: "book_library.db".

9. Import CSV Data: Imports book data from a csv file, e.g. book_data.csv.
   Then it then adds the data to the "book_library.db" database.

10. Export Database to CSV

11. End Program: Ends the program.

## ToDo:

- check if a book is in database before adding it, or add option do remove double entries

- Find a way to make it a standalone application. The pyinstaller package does not support zbar.

- fix that leading zeros are cut from ISBN

