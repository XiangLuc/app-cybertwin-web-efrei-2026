# App-Cybertwin-Web-Efrei-2026

Simulateur de risque cyber pour PME. L'application permet de visualiser les
actifs d'une entreprise, recenser ses vulnérabilités, calculer son niveau de
risque, consulter un tableau de bord et générer un rapport PDF.

Le projet est composé de deux parties :

- **`cybertwin-backend/`** — API REST (Flask + SQLAlchemy + MySQL)
- **`cybertwin-front/`** — Interface web (Vue + Vite)

## Architecture

```
cybertwin/
├── cybertwin-backend/   API REST Flask (port 5000)
└── cybertwin-front/     Interface Vue + Vite (port 5173)
```

Le frontend intéragit avec l'API du backend. **Il faut donc démarrer le backend
avant le frontend.**

## Ordre de démarrage

1. Lancer MySQL
2. Démarrer le **backend** (port 5000)
3. (Optionnel) Charger le jeu de données de démonstration
4. Démarrer le **frontend** (port 5173)

---

# Backend — CyberTwin (Flask)

API REST développée avec **Flask**, **SQLAlchemy** et **MySQL**, avec
authentification **JWT** par rôles et documentation **Swagger**.

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
cd cybertwin-backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1        # Windows PowerShell
pip install -r requirements.txt
```

> Sous macOS / Linux : `source .venv/bin/activate`

## 3. Configurer l'environnement

Crée un fichier `.env` à la racine du backend :

```
FLASK_APP=app.py
FLASK_DEBUG=level-de-logs (ex. 1)
PORT=votre-port-de-l-api (ex. 5000)
DATABASE_URL=lien-a-votre-base-de-donnees-mysql (ex : mysql+pymysql://user:password@localhost/cybertwin)
JWT_SECRET_KEY=votre-cle-secrete-pour-jwt
```

## 4. Lancer le serveur

```powershell
python app.py
```

L'API démarre sur **http://localhost:5000**.
Les tables sont créées automatiquement au premier démarrage (`db.create_all()`).

## 5. Charger le jeu de données (optionnel)

Un script Python `script_bdd.py` permet de remplir la base avec des données de
démonstration (entreprises, actifs, vulnérabilités et un compte par rôle).
Il **vide les tables** puis insère les données.

À lancer depuis le dossier du backend, **après** le premier démarrage du serveur
(pour que les tables existent) :

```powershell
python script_bdd.py
```

Comptes créés — mot de passe commun **`CyberTwin2024!`** (stocké haché en base) :

| Email                   | Rôle     |
|-------------------------|----------|
| admin@cybertwin.fr      | ADMIN    |
| analyste@cybertwin.fr   | ANALYSTE |
| lecteur@cybertwin.fr    | LECTEUR  |

## Documentation de l'API (Swagger)

Une fois le serveur lancé, la documentation est disponible sur :

```
http://localhost:5000/apidocs
```

Pour appeler les routes protégées : clique sur **Authorize**, puis colle
`Bearer <ton_token>` (le token est renvoyé par `POST /auth/login`).

## Stack technique (backend)

- **Flask** + **Flask-SQLAlchemy** (ORM) + **PyMySQL** (driver MySQL)
- **flask-jwt-extended** + **bcrypt** (authentification et hachage des mots de passe)
- **flasgger** (Swagger) + **flask-expects-json** (validation des entrées)

---

# Frontend — CyberTwin (Vue + Vite)

Interface du simulateur de risque cyber pour PME. Utilise l'API Flask en backend.

## Librairies principales

- Vue
- Vite
- Pinia
- Vue Router
- PrimeVue (UI)
- Axios
- jsPDF

## Prérequis

- Node.js version LTS et npm
- Le backend Flask CyberTwin démarré sur http://localhost:5000

## Installation

```bash
cd cybertwin-front
npm install
```

## Lancement

```bash
npm run dev
```

## Accès au projet en local

Ouvrir **http://localhost:5173** après le lancement.

## Comptes de démonstration

Si la base a été initialisée avec `script_bdd.py`, connecte-toi avec un des
comptes ci-dessus (mot de passe : `CyberTwin2024!`).