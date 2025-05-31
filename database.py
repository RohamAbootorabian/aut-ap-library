from app.application import app
import json

class database:
    def __init__(self, db_file_path="/Users/roham_abt/programming/python-programming/aut-ap-library/db.json"):
        self.db_file_path = db_file_path

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
        with open(self.db_file_path, "r") as file:
            data = json.load(file)
        return data.get("users", [])

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

    def save_books(self, users):
        """
        Save the list of users to the database.

        Args:
            books (list): List of users to save
        """
        with open(self.db_file_path, "r") as file:
            data = json.load(file)

        data["users"] = users

        with open(self.db_file_path, "w") as file:
            json.dump(data, file, indent=4)
