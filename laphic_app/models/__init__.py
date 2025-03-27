# laphic_app/models/__init__.py

from .user import User
from .service import Service  # Since you have multiple services (like renovation, construction, etc.), use Service as a general model.
from .Booking import Booking
from .provider import Provider
from .feedback import Feedback
from .message import Message

# Optional: if there are additional models, import them here

# Expose all models for easier import
__all__ = ["User", "Service", "Booking", "Provider", "Feedback", "Message"]
