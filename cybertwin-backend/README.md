# CyberTwin — Backend

API REST du simulateur de risque cyber pour PME **CyberTwin**.
Développée avec **Flask**, **SQLAlchemy** et **MySQL**, avec authentification
**JWT** par rôles et documentation **Swagger**.

## Prérequis

- **Python** ≥ 3.10
- **MySQL** (serveur démarré, ex. via WAMP / XAMPP / MySQL local)

## 1. Créer la base de données

Dans MySQL (phpMyAdmin ou ligne de commande), crée une base vide :

```sql
CREATE DATABASE cybertwin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 2. Installer les dépendances

Depuis le dossier du backend, crée et active un environnement virtuel, puis
installe les paquets :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1        # Windows PowerShell
pip install -r requirements.txt
```

> Sous macOS / Linux : `source .venv/bin/activate`

## 3. Configurer l'environnement

Crée un fichier `.env` à la racine du backend :

FLASK_APP=app.py
FLASK_DEBUG=level-de-logs (ex. 1)
PORT=votre-port-de-l-api (ex. 5000)
DATABASE_URL=lien-a-votre-base-de-donnees-mysql (ex : mysql+pymysql://user:password@localhost/cybertwin)
JWT_SECRET_KEY=votre-cle-secrete-pour-jwt

## 4. Lancer le serveur

```powershell
python app.py
```

L'API démarre sur **http://localhost:5000**.
Les tables sont créées automatiquement au premier démarrage (`db.create_all()`).
