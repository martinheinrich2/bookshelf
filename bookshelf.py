"""
Main Library code. Uses different modules to scan barcodes, collect data about
books.
"""
# %%
import scan_barcodes
import get_isbn_meta
import db_handler as db
import pandas as pd
import tkinter as tk
from tkinter import filedialog
# from tkinter import messagebox
import traceback
import os
from sqlalchemy import create_engine

# set database
db_name = 'BookDatabase.db'
database = db.Database("BookDatabase.db")
# %% Get list of ISBN numbers


def get_selected_row(event):
    try:
        global selected_row
        index = listbox.curselection()[0]
        selected_row = listbox.get(index)
        e0.delete(0, tk.END)
        e0.insert(tk.END, selected_row[0])
        e1.delete(0, tk.END)
        e1.insert(tk.END, selected_row[1])
        e2.delete(0, tk.END)
        e2.insert(tk.END, selected_row[2])
        e3.delete(0, tk.END)
        e3.insert(tk.END, selected_row[3])
        e4.delete(0, tk.END)
        e4.insert(tk.END, selected_row[4])
        e5.delete(0, tk.END)
        e5.insert(tk.END, selected_row[5])
        e6.delete(0, tk.END)
        e6.insert(tk.END, selected_row[6])
        e7.delete(0, tk.END)
        e7.insert(tk.END, selected_row[7])
        e8.delete(0, tk.END)
        e8.insert(tk.END, selected_row[8])
        T1.delete('1.0', tk.END)
        T1.update()
        T1.insert(tk.END, selected_row[9])
    except IndexError:
        pass


def readBarcodedata(filename):
    """
    Read barcodes from file if available
    Raises:
        ValueError: if no barcode.csv file is available
    """
    try:
        bcdf = pd.read_csv(filename, header=None)
        barcodes = bcdf.values.tolist()
    except IOError:
        raise ValueError("There is no file: " + filename)
    return barcodes

# %%


def get_bookData(codes):
    """ Gets data about book from google books

    Args:
        codes (type: list): [List of strings with ISBN codes]

    Returns:
        [pandas dataframe: [Pandas Dataframe with columns: Title, Subtitle,
        Author, Publisher, PubDate, Pages, ISBN10, ISBN13]
    """
    books = []
    for bar in codes:
        singlebarcode = str(bar)[1:-1]
        print(singlebarcode)
        book = [get_isbn_meta.main(singlebarcode)]
        print(book)
        # Do nothing if the book was not in Google Books, else add to list.
        # If there is no book, then book = [[]].
        if book == [[]]:
            print("List is empty!", book)
            continue
        else:
            books = books + book
            print(books)
    df = pd.DataFrame(books, columns=['Title', 'Subtitle', 'Author',
                                      'Publisher', 'PubDate', 'Pages',
                                      'ISBN10', 'ISBN13', 'Description'])
    return df


# %%
# Create Tkinter GUI

def clickedBscanner():
    '''
    Calls the barcode scanner module. Activates webcam to scan barcodes
    of books. Writes them into a file barcodes + timestamp.csv. Does not
    return anything.
    '''
    lbl.configure(text="Barcode scanner opens in separate window!", font=("Arial", 20))
    scan_barcodes.main()


def clickedGetBookdata():
    '''Read barcode file and get book metadata'''
    lbl.configure(text="Get book data from barcodes", font=("Arial", 20))
    filename = filedialog.askopenfilename()
    print(filename)
    barcodes = readBarcodedata(filename)
    df_books = get_bookData(barcodes)
    # create new file only if file does not exist, otherwise append
    if not os.path.isfile("book_data.csv"):
        df_books.to_csv("book_data.csv")
    else:
        df_books.to_csv("book_data.csv", mode='a', header=False)


def clickedCreatedb():
    table = 'books'
    param = 'book_id INTEGER UNIQUE, title TEXT, subtitle TEXT, author TEXT, publisher TEXT, pubdate TEXT, pages INTEGER, isbn10 INTEGER, isbn13 INTEGER, description TEXT, PRIMARY KEY(book_id)'
    database.createtable(table, param)
    database.close()


def clickedImport():
    filename = filedialog.askopenfilename()
    print(filename)
    book_df = pd.read_csv(filename, index_col=0)
    book_df.fillna('', inplace=True)
    book_df = book_df.drop_duplicates()
    engine = create_engine('sqlite:///BookDatabase.db')
    book_df.to_sql('books', con=engine, if_exists='append', index=False)


def clickedViewBooks():
    listbox.delete(0, tk.END)
    for row in database.view():
        listbox.insert(tk.END, row)


def clickedSearchBook():
    listbox.delete(0, tk.END)
    for row in database.search(title_text.get(), author_text.get()):
        listbox.insert(tk.END, row)


def clickedAdd():
    description = ""
    database.insert(title_text.get(), subtitle_text.get(), author_text.get(), publisher_text.get(), pubdate_text.get(), pages_text.get(), isbn10_text.get(), isbn13_text.get(), description)
    listbox.delete(0, tk.END)
    listbox.insert(tk.END, (title_text.get(), subtitle_text.get(), author_text.get(), publisher_text.get(), pubdate_text.get(), pages_text.get(), isbn10_text.get(), isbn13_text.get(), description))


def clickedUpdate():
    database.update(selected_row[0], title_text.get(), subtitle_text.get(), author_text.get(), publisher_text.get(), pubdate_text.get(), pages_text.get(), isbn10_text.get(), isbn13_text.get(), T1.get(1.0, "end-1c"))


def clickedDelete():
    database.delete(selected_row[0])


def clickedExport():
    database.writesqltocsv()


def clickedEnd():
    '''End program and close window'''
    root.destroy()

# You would normally put that on the App class


def show_error(self, *args):
    err = traceback.format_exception(*args)
    tk.messagebox.showerror('Error:', err)


# Create TKinter window
root = tk.Tk()
root.title("Bookshelf app")
lbl = tk.Label(root, text="Bookshelf",
               font=("Arial Bold", 30), fg="white", bg="blue")
lbl.grid(column=0, row=0)
root.geometry('900x580')

# Create Labels
l0 = tk.Label(root, text="ID")
l0.grid(row=0, column=1)
l1 = tk.Label(root, text="Title")
l1.grid(row=1, column=1)
l2 = tk.Label(root, text="Subtitle")
l2.grid(row=2, column=1)
l3 = tk.Label(root, text="Author")
l3.grid(row=3, column=1)
l4 = tk.Label(root, text="Publisher")
l4.grid(row=4, column=1)
l5 = tk.Label(root, text="Date Published")
l5.grid(row=5, column=1)
l6 = tk.Label(root, text="Pages")
l6.grid(row=6, column=1)
l7 = tk.Label(root, text="ISBN10")
l7.grid(row=7, column=1)
l8 = tk.Label(root, text="ISBN13")
l8.grid(row=8, column=1)
l9 = tk.Label(root, text="Description")
l9.grid(row=9, column=1)
l10 = tk.Label(root, text="List of Books")
l10.grid(row=13, column=1)


# Create events
id_text = tk.StringVar()
e0 = tk.Entry(root, textvariable=id_text, width=10)
e0.grid(row=0, column=2)
title_text = tk.StringVar()
e1 = tk.Entry(root, textvariable=title_text, width=50)
e1.grid(row=1, column=2)

subtitle_text = tk.StringVar()
e2 = tk.Entry(root, textvariable=subtitle_text, width=50)
e2.grid(row=2, column=2)

author_text = tk.StringVar()
e3 = tk.Entry(root, textvariable=author_text, width=50)
e3.grid(row=3, column=2)

publisher_text = tk.StringVar()
e4 = tk.Entry(root, textvariable=publisher_text, width=50)
e4.grid(row=4, column=2)

pubdate_text = tk.StringVar()
e5 = tk.Entry(root, textvariable=pubdate_text, width=50)
e5.grid(row=5, column=2)

pages_text = tk.IntVar()
e6 = tk.Entry(root, textvariable=pages_text, width=50)
e6.grid(row=6, column=2)

isbn10_text = tk.IntVar()
e7 = tk.Entry(root, textvariable=isbn10_text, width=50)
e7.grid(row=7, column=2)

isbn13_text = tk.IntVar()
e8 = tk.Entry(root, textvariable=isbn13_text, width=50)
e8.grid(row=8, column=2)

# create text widget for description of book
T1 = tk.Text(root, height=5, width=57)
T1.grid(row=9, column=2)
T1.config(font='arial 14', wrap='word')

# Create listbox to display list of books
listbox = tk.Listbox(root, height=8, width=50)
listbox.grid(row=13, column=2, rowspan=6, columnspan=2)

scrollbar = tk.Scrollbar(root)
scrollbar.grid(row=13, column=4, rowspan=8, sticky='ns')

listbox.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=listbox.yview)

listbox.bind('<<ListboxSelect>>', get_selected_row)


# Create buttons
btn1 = tk.Button(root, text="Scan barcode", width=20, command=clickedBscanner)
btn1.grid(column=0, row=1)
btn2 = tk.Button(root, text="Get book data from Google", width=20, command=clickedGetBookdata)
btn2.grid(column=0, row=2)
btn3 = tk.Button(root, text="View books", width=20, command=clickedViewBooks)
btn3.grid(column=0, row=4)
btn4 = tk.Button(root, text="Search title/author", width=20, command=clickedSearchBook)
btn4.grid(column=0, row=5)
btn5 = tk.Button(root, text="Add book", width=20, command=clickedAdd)
btn5.grid(column=0, row=6)
btn6 = tk.Button(root, text="Change data", width=20, command=clickedUpdate)
btn6.grid(column=0, row=7)
btn7 = tk.Button(root, text="Delete book", width=20, command=clickedDelete)
btn7.grid(column=0, row=8)
btn8 = tk.Button(root, text="Create database", width=20, command=clickedCreatedb)
btn8.grid(column=0, row=9)
btn9 = tk.Button(root, text="Import csv data", width=20, command=clickedImport)
btn9.grid(column=0, row=3)
btn10 = tk.Button(root, text="End program", width=20, command=clickedEnd)
btn10.grid(column=0, row=11)
btn11 = tk.Button(root, text="Export database to csv", width=20, command=clickedExport)
btn11.grid(column=0, row=10)
root.mainloop()
