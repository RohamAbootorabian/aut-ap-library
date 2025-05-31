from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

# Configure app settings
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


# Add a route to serve static files
@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)


# Add error handlers
@app.errorhandler(404)
def not_found_error(error):
    return {"error": "Resource not found"}, 404


@app.errorhandler(500)
def internal_error(error):
    return {"error": "Internal server error"}, 500
