# SyntheticData SaaS - Documentation Complète

##  Vue d'ensemble

**SyntheticData** est une plateforme SaaS permettant de générer des jeux de données **réalistes mais fictifs** à partir de schémas JSON personnalisés. Idéal pour les développeurs, testeurs et data engineers qui ont besoin de données de test sans utiliser de vraies informations.

---

##  Fonctionnalités principales

###  Génération de données
- Génération basée sur des schémas JSON personnalisables
- Support de 20+ types de champs (nom, email, téléphone, adresse, etc.)
- Export multi-formats : JSON, CSV, Excel, SQL, XML
- Génération de 1 à 50 000 lignes selon votre plan

###  Authentification & Gestion utilisateurs
- Inscription/Connexion sécurisée avec JWT
- Gestion de profil utilisateur
- Système de quotas par plan (Free/Pro/Enterprise)

###  Historique & Schémas
- Sauvegarde automatique des datasets générés
- Bibliothèque de schémas réutilisables
- Consultation et suppression de l'historique

---

##  Stack technologique

### Backend
- **Framework** : Django 5.x + Django REST Framework
- **Base de données** : PostgreSQL
- **Authentification** : JWT (SimpleJWT)
- **Génération de données** : Faker + Pandas
- **Export** : OpenPyXL, CSV, JSON, XML

### Frontend
- **Framework** : React 18 + Vite
- **Styling** : Tailwind CSS
- **Icons** : Lucide React
- **HTTP Client** : Axios
- **Routing** : React Router DOM

---

##  Structure du projet

```
syntheticdata-saas/
│
├── backend/                          # Backend Django
│   ├── config/                       # Configuration du projet
│   │   ├── settings.py              # Paramètres Django
│   │   ├── urls.py                  # URLs principales
│   │   └── wsgi.py                  # Point d'entrée WSGI
│   │
│   ├── users/                        # App gestion utilisateurs
│   │   ├── models.py                # Modèle User personnalisé
│   │   ├── serializers.py           # Serializers (Register, User)
│   │   ├── views.py                 # Vues (Register, Profile)
│   │   ├── urls.py                  # Routes authentification
│   │   └── admin.py                 # Config admin Django
│   │
│   ├── generator/                    # App génération de données
│   │   ├── models.py                # Modèles Schema et GeneratedDataset
│   │   ├── serializers.py           # Serializers génération
│   │   ├── views.py                 # Vues génération et historique
│   │   ├── urls.py                  # Routes API génération
│   │   ├── admin.py                 # Config admin
│   │   └── services/
│   │       ├── data_generator.py    # Logique génération avec Faker
│   │       └── file_exporter.py     # Export multi-formats
│   │
│   ├── subscriptions/                # App abonnements (futur Stripe)
│   │   ├── models.py                # Modèle Subscription
│   │   ├── admin.py                 # Config admin
│   │   └── stripe_service.py        # Intégration Stripe (à venir)
│   │
│   ├── manage.py                     # CLI Django
│   ├── requirements.txt              # Dépendances Python
│   └── .env                          # Variables d'environnement
│
└── frontend/                         # Frontend React
    ├── src/
    │   ├── components/              # Composants réutilisables
    │   │   ├── Navbar.jsx
    │   │   ├── Sidebar.jsx
    │   │   ├── DatasetForm.jsx
    │   │   └── DatasetTable.jsx
    │   │
    │   ├── pages/                   # Pages de l'application
    │   │   ├── Login.jsx
    │   │   ├── Register.jsx
    │   │   ├── Dashboard.jsx
    │   │   └── History.jsx
    │   │
    │   ├── services/                # Services API
    │   │   ├── api.js              # Configuration Axios + intercepteurs
    │   │   ├── authService.js      # Service authentification
    │   │   └── dataService.js      # Service génération données
    │   │
    │   ├── context/                 # Context API React
    │   │   └── AuthContext.jsx     # Context authentification
    │   │
    │   ├── App.jsx                  # Composant principal
    │   ├── main.jsx                 # Point d'entrée React
    │   └── index.css                # Styles Tailwind
    │
    ├── package.json                  # Dépendances npm
    └── vite.config.js               # Config Vite
```

---

##  Installation et Configuration

### Prérequis
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Git

###  Clone le repository

```bash
git clone https://github.com/ismailOu/syntheticDataSAAS.git
cd syntheticDataSAAS
```

### Configuration Backend

```bash
# Entre dans le dossier backend
cd backend

# Crée un environnement virtuel Python
python -m venv venv

# Active l'environnement virtuel
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Installe les dépendances
pip install -r requirements.txt
```

###  Configuration PostgreSQL

```sql
-- Crée la base de données
CREATE DATABASE syntheticdata_db;
CREATE USER syntheticdata_user WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE syntheticdata_db TO syntheticdata_user;
```

###  Fichier .env (backend)

Crée un fichier `.env` à la racine de `backend/` :

```env
SECRET_KEY=votre-cle-secrete-django-super-longue-et-aleatoire
DEBUG=True
DB_NAME=syntheticdata_db
DB_USER=syntheticdata_user
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=5432
```

** Générer une SECRET_KEY Django :**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

###  Migrations et Superuser

```bash
# Lance les migrations
python manage.py makemigrations
python manage.py migrate

# Crée un superuser admin
python manage.py createsuperuser

# Lance le serveur Django
python manage.py runserver
```

✅ Backend accessible sur : `http://127.0.0.1:8000`  
✅ Admin Django : `http://127.0.0.1:8000/admin`

###  Configuration Frontend

```bash
# Ouvre un nouveau terminal et va dans frontend
cd frontend

# Installe les dépendances
npm install

# Lance le serveur de développement
npm run dev
```

✅ Frontend accessible sur : `http://localhost:5173`

---

##  API Endpoints

### Authentification

| Méthode | Endpoint | Description | Auth requise |
|---------|----------|-------------|--------------|
| POST | `/api/auth/register/` | Inscription | ❌ |
| POST | `/api/auth/login/` | Connexion | ❌ |
| POST | `/api/auth/token/refresh/` | Refresh token JWT | ❌ |
| GET | `/api/auth/profile/` | Voir profil | ✅ |
| PUT | `/api/auth/profile/` | Modifier profil | ✅ |

### Génération de données

| Méthode | Endpoint | Description | Auth requise |
|---------|----------|-------------|--------------|
| POST | `/api/generate/` | Générer un dataset | ✅ |
| GET | `/api/schemas/` | Liste des schémas | ✅ |
| POST | `/api/schemas/` | Créer un schéma | ✅ |
| GET | `/api/schemas/{id}/` | Détail d'un schéma | ✅ |
| PUT | `/api/schemas/{id}/` | Modifier un schéma | ✅ |
| DELETE | `/api/schemas/{id}/` | Supprimer un schéma | ✅ |
| GET | `/api/history/` | Historique des datasets | ✅ |
| DELETE | `/api/history/{id}/` | Supprimer un dataset | ✅ |

---

## 🎨 Exemples d'utilisation API

### 1. Inscription

```bash
POST /api/auth/register/
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!"
}
```

**Réponse :**
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "plan": "free",
    "role": "user"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 2. Connexion

```bash
POST /api/auth/login/
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Réponse :**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Générer des données JSON

```bash
POST /api/generate/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "schema": {
    "nom": "name",
    "email": "email",
    "telephone": "phone_number",
    "pays": "country",
    "entreprise": "company"
  },
  "rows": 50,
  "format": "json",
  "save_schema": true,
  "schema_name": "Utilisateurs Test"
}
```

**Réponse :** Fichier JSON téléchargeable

```json
[
  {
    "nom": "Kossi Amegah",
    "email": "kossi.amegah@example.com",
    "telephone": "+228 90 12 34 56",
    "pays": "Togo",
    "entreprise": "TechHub Lomé"
  },
  {
    "nom": "Ama Djossou",
    "email": "ama.djossou@example.com",
    "telephone": "+228 91 45 67 89",
    "pays": "Togo",
    "entreprise": "Digital Solutions"
  }
  // ... 48 autres enregistrements
]
```

### 4. Générer des données CSV

```bash
POST /api/generate/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "schema": {
    "prenom": "first_name",
    "nom": "last_name",
    "email": "email",
    "ville": "city"
  },
  "rows": 100,
  "format": "csv"
}
```

**Réponse :** Fichier CSV téléchargeable

---

## 🔧 Types de champs disponibles

| Type | Description | Exemple |
|------|-------------|---------|
| `name` | Nom complet | "Jean Dupont" |
| `first_name` | Prénom | "Marie" |
| `last_name` | Nom de famille | "Martin" |
| `email` | Adresse email | "jean.dupont@example.com" |
| `phone_number` | Numéro de téléphone | "+33 6 12 34 56 78" |
| `address` | Adresse complète | "45 rue de la Paix, 75002 Paris" |
| `country` | Pays | "France" |
| `city` | Ville | "Lyon" |
| `date` | Date | "2024-01-15" |
| `datetime` | Date et heure | "2024-01-15T14:30:00" |
| `company` | Nom d'entreprise | "TechCorp SARL" |
| `job` | Métier | "Développeur Full-Stack" |
| `iban` | IBAN | "FR76 3000 6000 0112 3456 7890 189" |
| `credit_card` | Numéro de carte bancaire | "4532 1488 0343 6467" |
| `license_plate` | Plaque d'immatriculation | "AB-123-CD" |
| `text` | Texte aléatoire | "Lorem ipsum dolor sit..." |
| `paragraph` | Paragraphe | "Un paragraphe complet..." |
| `url` | URL | "https://example.com" |
| `ipv4` | Adresse IPv4 | "192.168.1.1" |
| `user_agent` | User agent | "Mozilla/5.0..." |
| `custom_text(N)` | Texte de N caractères | "Texte de 50 caractères..." |

---

## 🧪 Tests

### Backend - Test des services

```bash
# Test de génération manuelle
python test_generator.py

# Test complet de l'API
python test_api.py
```

### Backend - Tests Django (à créer)

```bash
python manage.py test
```

### Frontend - Tests (à configurer)

```bash
npm run test
```

---

## 🔒 Sécurité

### Backend
- ✅ Authentification JWT avec refresh token
- ✅ CORS configuré pour le frontend
- ✅ Validation des données avec Django REST Framework
- ✅ Protection CSRF
- ✅ Hashage sécurisé des mots de passe (Django Argon2)
- ✅ Variables sensibles dans .env
- ✅ HTTPS obligatoire en production

### Frontend
- ✅ Tokens stockés dans localStorage
- ✅ Intercepteurs Axios pour refresh automatique
- ✅ Protection des routes privées
- ✅ Validation côté client

---

## 📦 Déploiement

### Backend (Render / Railway)

1. **Créer un compte sur Render.com ou Railway.app**

2. **Fichier `requirements.txt` (vérifie qu'il contient) :**
```txt
Django==5.0.1
djangorestframework==3.14.0
django-cors-headers==4.3.1
djangorestframework-simplejwt==5.3.1
psycopg2-binary==2.9.9
python-decouple==3.8
faker==22.0.0
pandas==2.1.4
openpyxl==3.1.2
gunicorn==21.2.0
```

3. **Fichier `Procfile` (à la racine de backend/) :**
```
web: gunicorn config.wsgi
```

4. **Dans `settings.py`, ajoute :**
```python
import os

ALLOWED_HOSTS = ['*']  # À restreindre en production

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

5. **Variables d'environnement sur Render/Railway :**
- `SECRET_KEY`
- `DEBUG=False`
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

### Frontend (Vercel / Netlify)

1. **Créer un compte sur Vercel.com ou Netlify.com**

2. **Fichier `.env.production` (frontend/) :**
```env
VITE_API_URL=https://votre-backend.render.com/api
```

3. **Mettre à jour `src/services/api.js` :**
```js
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';
```

4. **Build et deploy :**
```bash
npm run build
```

5. **Connecter le repo GitHub à Vercel/Netlify**

---

## 🗓️ Roadmap MVP (12 jours)

| Phase | Tâche | Durée | Statut |
|-------|-------|-------|--------|
| 1 | Setup Django + DB + Faker | 2j | ✅ FAIT |
| 2 | API /generate/ | 2j | ✅ FAIT |
| 3 | Frontend formulaire + rendu | 3j | 🔄 EN COURS |
| 4 | Authentification JWT | 2j | ✅ FAIT |
| 5 | Historique + téléchargement | 2j | 🔄 EN COURS |
| 6 | Déploiement Render + Vercel | 1j | ⏳ À FAIRE |
| 7 | Intégration Stripe (optionnel) | 2j | ⏳ À FAIRE |

---

## 🚀 Évolutions futures

- [ ] IA générative pour schémas automatiques
- [ ] API GraphQL
- [ ] Application mobile (React Native)
- [ ] Éditeur visuel drag & drop
- [ ] Templates de datasets prêts à l'emploi
- [ ] Export vers bases de données (MySQL, MongoDB)
- [ ] Webhooks pour intégrations
- [ ] Collaboration en équipe
- [ ] Analytics et statistiques d'utilisation

---

## 🤝 Contribution

Les contributions sont les bienvenues ! 

1. Fork le projet
2. Crée une branche (`git checkout -b feature/AmazingFeature`)
3. Commit tes changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvre une Pull Request

---


## 👨‍💻 Auteur

**Ismaël Moussa**  
📧 Email: moussaisma05@gmail.com  
🌍 Localisation: Lomé, Togo

---

## 📞 Support

Pour toute question ou problème :
- 📧 Email: moussaisma05@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/votre-username/syntheticdata-saas/issues)

---

**⭐ Si ce projet vous est utile, n'hésitez pas à lui donner une étoile sur GitHub !**
