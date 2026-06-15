# Introduction à Alembic

Alembic est l’outil officiel de migration pour SQLAlchemy.

Son rôle est de gérer l’évolution de la structure de la base de données dans le temps.

---

# 1. Pourquoi Alembic ?

Avec SQLAlchemy, on peut créer les tables avec :

```python
Base.metadata.create_all(engine)
```

Mais cette méthode a une limite importante :

* elle crée les tables manquantes ;
* mais elle ne modifie pas les tables existantes.

Exemple :

Jour 1 :

```python
class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
```

Puis :

```python
Base.metadata.create_all(engine)
```

La table `users` est créée.

---

Jour 2 :

On ajoute :

```python
email: Mapped[str] = mapped_column(String(100))
```

Puis on relance :

```python
Base.metadata.create_all(engine)
```

La colonne `email` n’est PAS ajoutée.

Pourquoi ?

Parce que `create_all()` ne met pas à jour les tables existantes.

C’est exactement le problème qu’Alembic résout.

---

# 2. C’est quoi une migration ?

Une migration est un fichier qui décrit les modifications à appliquer sur la base de données.

Exemples :

* ajouter une colonne ;
* supprimer une colonne ;
* renommer une table ;
* ajouter une contrainte ;
* créer une nouvelle table.

Alembic permet donc de versionner la structure de la base de données.

---

# 3. Installation

Installer Alembic :

```bash
pip install alembic
```

---

# 4. Initialisation du projet Alembic

Dans le terminal :

```bash
alembic init alembic
```

Cela crée :

```text
alembic/
alembic.ini
```

---

# 5. Configuration de la connexion

Dans `alembic.ini` :

```ini
sqlalchemy.url = postgresql+psycopg://postgres:password@localhost:5432/alchemy_demo
```

Format :

```text
postgresql+psycopg://user:password@host:port/database
```

---

# 6. Lier Alembic aux modèles SQLAlchemy

Dans `alembic/env.py`, remplacer :

```python
target_metadata = None
```

par :

```python
from db.database import Base

target_metadata = Base.metadata
```

Important :

Les modèles doivent aussi être importés pour qu’Alembic les connaisse.

Exemple :

```python
from models.users import Users
from models.profiles import Profiles
```

---

# 7. Générer une migration

Après modification des modèles :

```bash
alembic revision --autogenerate -m "add email to users"
```

Explication :

* `revision` crée une migration ;
* `--autogenerate` compare les modèles Python avec la base ;
* `-m` ajoute un message descriptif.

Alembic crée alors un fichier dans :

```text
alembic/versions/
```

---

# 8. Exemple de migration générée

```python
def upgrade():
    op.add_column(
        'users',
        sa.Column('email', sa.String(length=100), nullable=True)
    )

def downgrade():
    op.drop_column('users', 'email')
```

---

# 9. Appliquer les migrations

Pour appliquer toutes les migrations :

```bash
alembic upgrade head
```

`head` signifie :

> dernière version des migrations.

---

# 10. Downgrade

Alembic peut aussi revenir en arrière.

Exemple :

```bash
alembic downgrade -1
```

Cela annule la dernière migration.

---

# 11. Erreur fréquente : NOT NULL

Exemple :

```python
favorite_color: Mapped[str] = mapped_column(String(50))
```

Avec SQLAlchemy 2.x :

```python
Mapped[str]
```

implique automatiquement :

```sql
NOT NULL
```

Si la table contient déjà des lignes, PostgreSQL peut refuser d’ajouter cette colonne :

```text
column contains null values
```

Pourquoi ?

Parce que les anciennes lignes n’ont aucune valeur pour cette nouvelle colonne.

Solutions possibles :

## Autoriser NULL

```python
favorite_color: Mapped[str | None]
```

ou :

```python
mapped_column(String(50), nullable=True)
```

---

## Donner une valeur par défaut

Dans la migration :

```python
op.add_column(
    'users',
    sa.Column(
        'favorite_color',
        sa.String(length=50),
        nullable=False,
        server_default='unknown'
    )
)
```

---

# 12. Workflow typique

```text
Modifier les modèles Python
↓
Créer une migration
↓
Vérifier le fichier généré
↓
Appliquer la migration
```

Commandes :

```bash
alembic revision --autogenerate -m "message"
```

```bash
alembic upgrade head
```

---

# 13. Résumé

Alembic sert à :

* gérer les changements de structure de la DB ;
* versionner les tables ;
* créer des migrations ;
* mettre à jour la base proprement.

Commandes essentielles :

```bash
alembic init alembic
```

```bash
alembic revision --autogenerate -m "message"
```

```bash
alembic upgrade head
```

```bash
alembic downgrade -1
```

---

# 14. Points importants et limites

## Limites de `--autogenerate`

Alembic peut détecter beaucoup de changements automatiquement, mais pas tous.

Exemples :
- renommage de colonnes ;
- renommage de tables ;
- certaines contraintes complexes ;
- changements très spécifiques.

Il faut donc toujours vérifier le fichier de migration généré avant de l’appliquer.

---

## Détection des changements de type

Par défaut, Alembic ne détecte pas toujours les changements de type.

Exemple :

String(50) -> String(100)

Pour améliorer cela, on peut activer :

compare_type=True

dans `alembic/env.py`.

Exemple :

```python

# Dans alembic/env.py, ajoutez compare_type=True dans context.configure()
# (Généralement présent dans run_migrations_offline et run_migrations_online)

context.configure(
    connection=connection,
    target_metadata=target_metadata,
    compare_type=True  # Permet de détecter le passage de String(50) à String(100)
)

```

---

## Variables d’environnement

Dans un vrai projet, on évite de mettre directement les mots de passe dans `alembic.ini`.

On utilise généralement :
- un fichier `.env` ;
- ou des variables d’environnement système.

Exemple dans `env.py` :

```python

from dotenv import load_dotenv
import os

load_dotenv()

# Récupération de l'URL depuis le .env ou reconstruction dynamique
db_url = os.getenv("DATABASE_URL") 
# Ou alternativement : f"postgresql+psycopg://{os.getenv('DB_USER')}..."

# Injection dynamique de l'URL dans la configuration d'Alembic
config.set_main_option("sqlalchemy.url", db_url)

```

---

## Commandes utiles

Voir la migration actuelle :

alembic current

Voir l’historique des migrations :

alembic history

Voir la SQL générée sans l’exécuter :

alembic upgrade head --sql

---

## Important : vérifier les migrations générées

Même avec `--autogenerate`, Alembic n’est pas magique.

Il faut toujours lire le fichier généré dans :

alembic/versions/

avant de faire :

alembic upgrade head

Car une mauvaise migration peut :
- supprimer des données ;
- casser une table ;
- provoquer une erreur SQL.

---

## Comparaison avec Git

Alembic peut être vu comme un système de versionnement pour la structure de la base de données.

Git versionne :
- les fichiers du projet.

Alembic versionne :
- les changements du schéma SQL.

Chaque migration représente une étape de l’évolution de la base.