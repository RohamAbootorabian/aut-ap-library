from app.application import app
import os
import json

# Resolve db.json next to this file so the app runs from any directory
# and on any machine. Override with the DB_PATH environment variable.
DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db.json")


class database:
    def __init__(self, db_file_path=None):
        self.db_file_path = db_file_path or os.environ.get("DB_PATH", DEFAULT_DB_PATH)
        self._initialize_db()

    def _initialize_db(self):
        """
        Initialize the database file if it doesn't exist.
        """
        if not os.path.exists(self.db_file_path):
            with open(self.db_file_path, "w") as file:
                json.dump({"users": [], "books": []}, file, indent=4)

    def get_all_books(self):
        """
        Get all books from the database.

        Returns:
            list: List of books
        """
        with open(self.db_file_path, "r") as file:
            data = json.load(file)
        return data.get("books", [])
    
    def get_all_users(self):
        """
        Get all users from the database.

        Returns:
            list: List of users
        """
        try:
            with open(self.db_file_path, "r") as file:
                data = json.load(file)
            return data.get("users", [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            app.logger.error(f"Error reading users from database: {str(e)}")
            return []

    def save_books(self, books):
        """
        Save the list of books to the database.

        Args:
            books (list): List of books to save
        """
        with open(self.db_file_path, "r") as file:
            data = json.load(file)

        data["books"] = books

        with open(self.db_file_path, "w") as file:
            json.dump(data, file, indent=4)

    def save_users(self, users):
        """
        Save the list of users to the database.

        Args:
            users (list): List of users to save
        """
        with open(self.db_file_path, "r") as file:
            data = json.load(file)

        data["users"] = users

        with open(self.db_file_path, "w") as file:
            json.dump(data, file, indent=4)
