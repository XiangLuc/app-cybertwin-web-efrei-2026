"""
Point d'entree de l'application CyberTwin.

"""
import os
from sqlite3 import OperationalError
import sys

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from controllers.entreprise_controller import entreprise_bp
from controllers.actif_controller import actif_bp
from controllers.vulnerabilite_controller import vulnerabilite_bp
from controllers.analyse_controller import analyse_bp
from controllers.auth_controller import auth_bp
from controllers.notification_controller import notification_bp

from infra.db.database import db
from utils.swagger_config import swagger_config, swagger_template

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_SORT_KEYS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

cors = CORS(app)
db.init_app(app)
swagger = Swagger(app, template=swagger_template, config=swagger_config)

app.register_blueprint(entreprise_bp, url_prefix="/company")
app.register_blueprint(actif_bp, url_prefix="/assets")
app.register_blueprint(vulnerabilite_bp, url_prefix="/vulnerabilities")
app.register_blueprint(analyse_bp)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(notification_bp, url_prefix="/notifications")

jwt = JWTManager(app)


@app.errorhandler(400)
def handle_validation_error(error):
    """Renvoie en JSON les erreurs de validation levees par flask_expects_json."""
    description = getattr(error, "description", str(error))
    message = getattr(description, "message", str(description))
    return jsonify({"error": message}), 400


with app.app_context():
    try:
        db.create_all()
        print("INFO : Connexion à la base de données réussie.")
    except OperationalError as e:
        print("\nERREUR : Connexion à la base de données impossible.")
        sys.exit(1)
    except Exception as e:
        print(f"\nERREUR : Problème inattendu avec la base de données.\nDétails : {e}\n")
        sys.exit(1)


@app.route("/")
def index():
    return jsonify({"name": "CyberTwin API", "status": "ok", "docs": "/apidocs"})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=os.getenv("FLASK_DEBUG", "1") == "1",
    )