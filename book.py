from flask import Flask, request
import sqlite3

app = Flask(__name__)


def connect():
    return sqlite3.connect("books.db")


# Create table
def create_table():
    con = connect()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            price REAL
        )
    """)

    con.commit()
    con.close()


# Home - Display books
@app.route("/")
def home():

    con = connect()
    cur = con.cursor()

    cur.execute("SELECT * FROM books")
    books = cur.fetchall()

    con.close()

    result = "<h1>Book Management System</h1>"

    result += """
    <a href="/add">Add Book</a>
    <br><br>
    """

    result += """
    <table border="1">
    <tr>
        <th>ID</th>
        <th>Title</th>
        <th>Author</th>
        <th>Price</th>
        <th>Action</th>
    </tr>
    """

    for book in books:
        result += f"""
        <tr>
            <td>{book[0]}</td>
            <td>{book[1]}</td>
            <td>{book[2]}</td>
            <td>{book[3]}</td>
            <td>
                <a href="/delete/{book[0]}">Delete</a>
            </td>
        </tr>
        """

    result += "</table>"

    return result


# Add book
@app.route("/add", methods=["GET", "POST"])
def add_book():

    if request.method == "POST":

        title = request.form["title"]
        author = request.form["author"]
        price = request.form["price"]

        con = connect()
        cur = con.cursor()

        cur.execute("""
            INSERT INTO books(title, author, price)
            VALUES (?, ?, ?)
        """, (title, author, price))

        con.commit()
        con.close()

        return "Book added successfully! <br><a href='/'>View Books</a>"

    return """
    <h1>Add Book</h1>

    <form method="POST">

        Book Title:
        <input type="text" name="title">
        <br><br>

        Author:
        <input type="text" name="author">
        <br><br>

        Price:
        <input type="number" name="price">
        <br><br>

        <input type="submit" value="Add Book">

    </form>

    <br>
    <a href="/">Back</a>
    """


# Delete book
@app.route("/delete/<int:id>")
def delete_book(id):

    con = connect()
    cur = con.cursor()

    cur.execute("DELETE FROM books WHERE id = ?", (id,))

    con.commit()
    con.close()

    return "Book deleted successfully! <br><a href='/'>View Books</a>"


if __name__ == "__main__":

    create_table()

    app.run(debug=True)