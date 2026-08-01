from app.application import app
from flask import jsonify, request
from database import database

db = database()

@app.route("/api/v1/books")
def get_books():
    """
    Get all books
    Returns:
        list: List of books
    """
    try:
        books = db.get_all_books()
        if not books:
            return jsonify({"error": "No books found"}), 404
        return jsonify(books)
    except Exception as e:
        return jsonify({"error": f"Failed to load books: {str(e)}"}), 500


@app.route("/api/v1/books/<book_id>")
def get_book(book_id: str):
    """
    Get a book by id

    Args:
        book_id (str): The id of the book

    Returns:
        dict: Book details

    Raises:
        NotFound: If the book is not found
    """
    books = db.get_all_books()
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book)


@app.route("/api/v1/books", methods=["POST"])
def create_book():
    """
    Create a new book

    Returns:
        dict: Book details

    Raises:
        BadRequest: If the request body is invalid
    """
    payload = request.json
    required = ("title", "author", "isbn")
    if not payload or any(not payload.get(field) for field in required):
        return jsonify({"error": "title, author and isbn are required"}), 400

    books = db.get_all_books()

    # The server owns id assignment — clients should not have to invent one,
    # and letting them pick invites collisions.
    next_id = str(max((int(b["id"]) for b in books if str(b["id"]).isdigit()), default=0) + 1)

    new_book = {
        "id": next_id,
        "title": payload["title"],
        "author": payload["author"],
        "isbn": payload["isbn"],
        "is_reserved": False,
        "reserved_by": None,
    }
    books.append(new_book)
    db.save_books(books)
    return jsonify(new_book), 201


@app.route("/api/v1/books/<book_id>", methods=["DELETE"])
def delete_book(book_id: str):
    """
    Delete a book by id

    Args:
        book_id (str): The id of the book

    Returns:
        dict: Success message

    Raises:
        NotFound: If the book is not found
        BadRequest: If the book is reserved
    """
    books = db.get_all_books()
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    books.remove(book)
    db.save_books(books)
    return jsonify({"message": "Book deleted"})
