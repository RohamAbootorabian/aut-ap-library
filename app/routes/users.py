from app.application import app
from flask import jsonify, request
from database import database

db = database()

@app.route("/api/v1/users")
def get_users():
    """
    Get all users
    Returns:
        list: List of users
    """
    try:
        users = db.get_all_users()
        if not users:
            return jsonify({"error": "No users found"}), 404
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": f"Failed to load users: {str(e)}"}), 500


@app.route("/api/v1/users/<user_id>")
def get_user(user_id: str):
    """
    Get a user by id

    Args:
        user_id (str): The id of the user

    Returns:
        dict: user details

    Raises:
        NotFound: If the user is not found
    """
    users = db.get_all_users()
    user = next((b for b in users if b["id"] == user_id), None)
    if not user:
        return jsonify({"error": "user not found"}), 404
    return jsonify(user)


@app.route("/api/v1/users", methods=["POST"])
def create_user():
    """
    Create a new user

    Returns:
        dict: user details

    Raises:
        BadRequest: If the request body is invalid
    """
    new_user = request.json
    if not new_user or "id" not in new_user or "title" not in new_user:
        return jsonify({"error": "Invalid user data"}), 400

    books = db.get_all_users()
    if any(b["id"] == new_user["id"] for b in users):
        return jsonify({"error": "user with this ID already exists"}), 400

    books.append(new_user)
    db.save_users(users)
    return jsonify(new_user), 201


@app.route("/api/v1/users/<user_id>", methods=["DELETE"])
def delete_user(user_id: str):
    """
    Delete a user by id

    Args:
        user_id (str): The id of the user

    Returns:
        dict: Success message

    Raises:
        NotFound: If the user is not found
        BadRequest: If the user is reserved
    """
    users = db.get_all_users()
    user = next((b for b in users if b["id"] == user_id), None)
    if not user:
        return jsonify({"error": "user not found"}), 404

    users.remove(user)
    db.save_users(users)
    return jsonify({"message": "user deleted"})
