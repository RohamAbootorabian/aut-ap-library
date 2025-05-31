from .application import app

# import routes after app is created to avoid circular imports
from .routes.books import *  # Import book-related routes
from .routes.users import *  # Import user-related routes
from .routes.reservation import *  # Import reservation-related routes
