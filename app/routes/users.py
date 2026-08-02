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
    payload = request.json
    required = ("username", "name", "email")
    if not payload or any(not payload.get(field) for field in required):
        return jsonify({"error": "username, name and email are required"}), 400

    users = db.get_all_users()
    if any(u["username"] == payload["username"] for u in users):
        return jsonify({"error": "Username already taken"}), 400

    next_id = str(max((int(u["id"]) for u in users if str(u["id"]).isdigit()), default=0) + 1)

    new_user = {
        "id": next_id,
        "username": payload["username"],
        "name": payload["name"],
        "email": payload["email"],
        "reserved_books": [],
    }
    users.append(new_user)
    db.save_users(users)
    return jsonify(new_user), 201


@app.route("/api/v1/users/<user_id>", methods=["PUT"])
def update_user(user_id: str):
    """
    Update a user by id

    Args:
        user_id (str): The id of the user

    Returns:
        dict: The updated user

    Raises:
        BadRequest: If the request body is invalid or the username is taken
        NotFound: If the user is not found
    """
    payload = request.json
    required = ("username", "name", "email")
    if not payload or any(not payload.get(field) for field in required):
        return jsonify({"error": "username, name and email are required"}), 400

    users = db.get_all_users()
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # A username has to stay unique, but the user keeping their own is fine
    taken = any(
        u["username"] == payload["username"] and u["id"] != user_id for u in users
    )
    if taken:
        return jsonify({"error": "Username already taken"}), 400

    user["username"] = payload["username"]
    user["name"] = payload["name"]
    user["email"] = payload["email"]
    db.save_users(users)
    return jsonify(user)


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
