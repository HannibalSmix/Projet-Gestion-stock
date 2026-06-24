# Projet Gestion Stock

Application de gestion de stock en Python avec SQLAlchemy (ORM 2.0) et PostgreSQL.

## Fonctionnalités

- Gestion des entrepôts, fournisseurs et produits
- Réceptions de marchandises (`Receipt` / `ReceiptLine`)
- Transferts inter-entrepôts (`Transfert` / `TransfertLine`)
- Suivi des niveaux de stock (`Stocklevel`)
- Historique des mouvements de stock (`Stockmove`)
- Export des données en CSV

## Stack technique

- **Python 3.11**
- **SQLAlchemy 2.0** (syntaxe `Mapped[]` / `mapped_column`)
- **Alembic** pour les migrations
- **PostgreSQL** comme base de données
- **python-dotenv** pour la gestion des variables d'environnement

## Structure du projet

```
Projet-Gestion-stock/
│
├── .env                    # Variables d'environnement (DATABASE_URL)
├── alembic.ini              # Configuration Alembic
├── requirements.txt
├── seed.py                  # Script de génération de données de test
│
├── alembic/
│   ├── env.py
│   └── versions/             # Fichiers de migration
│
├── db/
│   ├── base.py               # Déclaration de Base (SQLAlchemy)
│   └── database.py           # Engine, session, imports des modèles
│
├── models/                   # Modèles SQLAlchemy (un fichier par table)
│   ├── ...
│
├── crud/                     # Fonctions CRUD (accès DB simple)
│   ├── ...
│
├── services/                 # Logique métier (orchestration de plusieurs CRUDs)
│   ├── receipt_services.py    # Validation des réceptions
│   └── transfert_services.py  # Validation des transferts
│
└── utils/
    └── export_csv.py          # Export des données en CSV
```

## Installation

1. Cloner le projet et créer un environnement virtuel :
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   ```

2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Créer un fichier `.env` à la racine avec l'URL de connexion à la base :
   ```env
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_HOST=
    POSTGRES_PORT=
    POSTGRES_DB=
   ```

4. Appliquer les migrations :
   ```bash
   alembic upgrade head
   ```

5. (Optionnel) Peupler la base avec des données de test :
   ```bash
   python seed.py
   ```

## Logique métier

### Réception (`Receipt`)

Une réception passe par les statuts `DRAFT → DONE` ou `DRAFT → CANCELLED`.

La validation d'une réception (`validate_receipt`) :
1. Vérifie que la réception est en `DRAFT`
2. Met à jour le `Stocklevel` pour chaque produit reçu
3. Crée un `Stockmove` de type `IN` pour chaque ligne
4. Passe la réception en `DONE`

### Transfert (`Transfert`)

Un transfert déplace du stock d'un entrepôt source vers un entrepôt destination.

La validation d'un transfert (`validate_transfert`) :
1. Vérifie que le transfert est en `DRAFT`
2. Vérifie que le stock est suffisant dans l'entrepôt source pour toutes les lignes
3. Débite l'entrepôt source et crédite l'entrepôt destination
4. Crée un `Stockmove` de type `TRANSFER` pour chaque ligne
5. Passe le transfert en `DONE`

## Migrations (Alembic)

Créer une nouvelle migration après modification des modèles :
```bash
alembic revision --autogenerate -m "description du changement"
alembic upgrade head
```