"""Flask extension instances.

Extensions are instantiated here and initialized with the app
in the factory (``create_app``).  Importing ``db`` from this module
gives access to the Flask-SQLAlchemy instance everywhere.
"""

from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy

from domain.models.base import Base

db = SQLAlchemy(model_class=Base)
