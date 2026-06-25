"""Instance SQLAlchemy partagee par toute l'application."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()