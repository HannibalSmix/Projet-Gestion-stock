# Introduction à SQLAlchemy

Ce projet sert de base pour apprendre SQLAlchemy avec Python et PostgreSQL.

Objectifs du cours :

- comprendre le rôle de SQLAlchemy ;
- connecter Python à une base PostgreSQL ;
- déclarer des tables avec des classes Python ;
- ouvrir une session de travail avec la base ;
- créer, lire, modifier et supprimer des données ;
- comprendre les requêtes avec `select()` et les objets `stmt` ;
- manipuler une relation simple entre deux tables.

---

## 1. C'est quoi SQLAlchemy ?

SQLAlchemy est une bibliothèque Python qui permet de travailler avec une base de données SQL.

Elle peut être utilisée de deux manières principales :

- **SQLAlchemy Core** : on écrit des requêtes SQL en Python avec des objets.
- **SQLAlchemy ORM** : on manipule des classes Python qui représentent des tables.

Dans ce projet, on utilise surtout l'ORM.

Schéma mental à retenir :

```text
Table SQL   <-> Classe Python
Ligne SQL   <-> Objet Python
Colonne SQL <-> Attribut Python
```

Exemple :

```python
user = Users(username="Alice", email="alice@mail.com")
session.add(user)
session.commit()
```

Ici, on crée un objet Python, mais SQLAlchemy va le transformer en ligne dans la table `users`.

---

## 2. Installation

Créer un environnement virtuel :

```bash
python -m venv venv
```

Activer l'environnement virtuel sous Windows :

```bash
venv\Scripts\activate
```

Installer les dépendances :

```bash
pip install sqlalchemy "psycopg[binary]" python-dotenv
```

Ou installer depuis le fichier `requirements.txt` :

```bash
pip install -r requirements.txt
```

Dépendances principales :

- `SQLAlchemy` : ORM et outils SQL.
- `psycopg` : driver PostgreSQL pour Python.
- `python-dotenv` : lecture du fichier `.env`.

---

## 3. Configuration de la base de données

Le projet utilise un fichier `.env` pour stocker les informations de connexion.

Exemple :

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=alchemy_demo
```

Ces variables sont ensuite lues dans `db/database.py`.

```python
from dotenv import load_dotenv
import os

load_dotenv()
```

`load_dotenv()` charge les variables du fichier `.env` dans l'environnement Python.

---

## 4. DATABASE_URL

SQLAlchemy a besoin d'une URL de connexion.

```python
DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)
```

Format général :

```text
postgresql+psycopg://user:password@host:port/database
```

Exemple :

```text
postgresql+psycopg://postgres:postgres@localhost:5432/alchemy_demo
```

---

## 5. Engine

L'`engine` est l'objet qui représente la connexion entre SQLAlchemy et la base de données.

```python
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL, echo=False)
```

Rôle de l'engine :

- connaître l'adresse de la base ;
- gérer les connexions ;
- envoyer les requêtes SQL ;
- recevoir les résultats.

Option utile :

```python
engine = create_engine(DATABASE_URL, echo=True)
```

Avec `echo=True`, SQLAlchemy affiche les requêtes SQL générées dans le terminal. C'est très utile pour apprendre.

---

## 6. Base déclarative

SQLAlchemy ORM a besoin d'une classe de base pour déclarer les modèles.

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

Toutes les classes qui représentent des tables vont hériter de `Base`.

Exemple :

```python
class Users(Base):
    __tablename__ = "users"
```

Cela permet à SQLAlchemy de connaître toutes les tables du projet.

---

## 7. Création des tables

Dans `main.py`, on trouve :

```python
Base.metadata.create_all(engine)
```

Signification :

- `Base.metadata` contient la description des tables déclarées avec les modèles.
- `create_all(engine)` demande à SQLAlchemy de créer ces tables dans la base.

Deux points importants à retenir :

- `create_all()` est pratique pour débuter, mais dans un vrai projet on utilise plutôt un outil de migration comme **Alembic** — on en reparlera dans un cours avancé.
- `create_all()` crée les tables manquantes, mais **ne met pas à jour** les tables existantes si le modèle change. Par exemple, si on ajoute une colonne dans une classe Python après la création de la table, `create_all()` ne va pas modifier automatiquement cette table.

---

## 8. Session

La session est l'objet principal pour travailler avec la base.

```python
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine)
```

`SessionLocal` est une fabrique de sessions.

Pour ouvrir une session :

```python
with SessionLocal() as session:
    ...
```

Rôle de la session :

- ajouter des objets ;
- exécuter des requêtes ;
- modifier des données ;
- supprimer des données ;
- valider ou annuler une transaction.

La session garde temporairement les changements en mémoire. Rien n'est définitivement enregistré tant qu'on n'a pas fait :

```python
session.commit()
```

---

## 9. Modèle `Users`

Un modèle est une classe Python qui représente une table SQL.

```python
class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)
    country: Mapped[str] = mapped_column(String(50), nullable=True)
```

Explication :

- `__tablename__` donne le nom de la table.
- `Mapped[int]` indique le type Python attendu.
- `mapped_column()` déclare une colonne SQL.
- `primary_key=True` indique la clé primaire.
- `unique=True` interdit les doublons.
- `nullable=False` interdit `NULL`.
- `String(50)` crée une colonne texte de maximum 50 caractères.

---

## 10. Méthode `__repr__`

Quand on affiche un objet Python, Python utilise sa représentation.

Sans `__repr__`, un objet SQLAlchemy peut s'afficher comme ceci :

```text
<models.users.Users object at 0x000001A2B3C4D5E0>
```

Ce n'est pas lisible pour un débutant.

On peut donc ajouter :

```python
def __repr__(self):
    return f"Users(id={self.id}, username='{self.username}')"
```

Comme ça, quand on fait :

```python
print(user)
```

On obtient une sortie claire :

```text
Users(id=1, username='Alice')
```

`__repr__` ne change pas la base de données. Il sert seulement à mieux afficher les objets Python.

---

## 11. Modèle `Profiles`

```python
class Profiles(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    bio: Mapped[str] = mapped_column(String(500))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )
```

`user_id` est une clé étrangère vers la table `users`.

```python
ForeignKey("users.id")
```

Cela veut dire :

> chaque profil appartient à un utilisateur.

Le `unique=True` sur `user_id` force une relation one-to-one :

> un utilisateur ne peut avoir qu'un seul profil.

---

## 12. Relations

Dans `Users` :

```python
profil: Mapped["Profiles"] = relationship(
    "Profiles",
    back_populates="user",
    uselist=False
)
```

Dans `Profiles` :

```python
user: Mapped["Users"] = relationship(
    "Users",
    back_populates="profil"
)
```

Explication :

- `relationship()` crée un lien Python entre deux modèles.
- `back_populates` relie les deux côtés de la relation.
- `uselist=False` indique qu'un utilisateur a un seul profil, pas une liste.

Par défaut, `relationship()` peut retourner une liste quand la relation pointe vers plusieurs objets. Avec `uselist=False`, on indique à SQLAlchemy que la relation est one-to-one : on récupère un seul objet au lieu d'une liste.

Grâce à ça, on peut faire :

```python
user.profil
profil.user
```
```Errata
    # Mapped["Transfert"] (objet seul) → SQLAlchemy comprend que c'est one-to-one.
    # Mapped[list["Transfert"]] (liste) → SQLAlchemy comprend que c'est one-to-many.
```

---

## 13. CRUD

CRUD signifie :

- **Create** : créer une donnée.
- **Read** : lire une donnée.
- **Update** : modifier une donnée.
- **Delete** : supprimer une donnée.

---

## 14. Create

Exemple avec `create_user()` :

```python
def create_user(session: Session, username: str, email: str, country: str):
    user = Users(username=username, email=email, country=country)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
```

Étapes :

1. On crée un objet Python.
2. `session.add(user)` ajoute l'objet dans la session.
3. `session.commit()` enregistre en base.
4. `session.refresh(user)` recharge l'objet depuis la base.
5. On retourne l'utilisateur créé.

Pourquoi `refresh()` ?

La base peut générer certaines valeurs automatiquement, comme `id`. `refresh()` relit l'objet depuis la base de données pour récupérer ces valeurs.

Important : `refresh()` ne sauvegarde pas. C'est `commit()` qui enregistre les changements.

---

## 15. Read avec `select()`

SQLAlchemy 2.x utilise beaucoup `select()`.

```python
from sqlalchemy import select

stmt = select(Users)
```

`stmt` signifie souvent "statement".

Un `stmt` est une requête SQL construite en Python.

```python
stmt = select(Users).where(Users.username == username)
```

Cette requête correspond environ à :

```sql
SELECT * FROM users WHERE username = 'Alice';
```

Mais on ne l'écrit pas en SQL brut. SQLAlchemy construit la requête proprement.

---

## 16. Exécuter une requête

Pour exécuter un `stmt` :

```python
result = session.execute(stmt)
```

`execute()` retourne un objet `Result` SQLAlchemy.

Ensuite, on choisit comment récupérer le résultat.

Un seul objet ou `None` :

```python
user = session.execute(stmt).scalar_one_or_none()
```

Tous les objets :

```python
users = session.execute(stmt).scalars().all()
```

Différence importante :

- `execute(stmt)` exécute la requête.
- `execute(stmt)` retourne d'abord des lignes SQLAlchemy, pas directement une liste d'objets.
- `scalars()` récupère directement les objets ORM.
- `all()` récupère tous les résultats.
- `scalar_one_or_none()` récupère un seul résultat ou `None`.

---

## 16.1 `scalar_one()`, `scalar_one_or_none()` et `first()`

Après l'exécution d'une requête, SQLAlchemy propose plusieurs façons de récupérer les résultats.

### `scalar_one()`

```
stmt = select(Users).where(Users.id == 1)

user = session.execute(stmt).scalar_one()
```

Comportement :

* retourne exactement un objet ;
* lève une exception si aucun résultat n'est trouvé ;
* lève une exception si plusieurs résultats sont trouvés.

À utiliser lorsqu'on est certain qu'une seule ligne doit exister.

### `scalar_one_or_none()`

```
stmt = select(Users).where(Users.username == username)

user = session.execute(stmt).scalar_one_or_none()
```

Comportement :

* retourne l'objet trouvé ;
* retourne `None` si aucun résultat n'existe ;
* lève une exception si plusieurs résultats sont trouvés.

Très pratique pour rechercher une ligne unique.

### `first()`

```
stmt = select(Users)

user = session.execute(stmt).scalars().first()
```

Comportement :

* retourne le premier résultat trouvé ;
* retourne `None` si aucun résultat n'existe ;
* ne vérifie pas qu'il n'existe qu'une seule ligne.

À utiliser lorsqu'on souhaite simplement récupérer le premier résultat.

Résumé :

| Méthode                | 0 résultat | 1 résultat    | Plusieurs résultats |
| ---------------------- | ---------- | ------------- | ------------------- |
| `scalar_one()`         | erreur     | objet         | erreur              |
| `scalar_one_or_none()` | `None`     | objet         | erreur              |
| `first()`              | `None`     | premier objet | premier objet       |

---

## 16.2 Le cycle de vie des objets ORM

Un objet SQLAlchemy passe par plusieurs états au cours de sa vie.

### Transient

Objet créé mais non connu de la session.

```
user = Users(
    username="Alice",
    email="alice@mail.com"
)
```

L'objet existe uniquement en mémoire Python.

### Pending

Objet ajouté à la session.

```
session.add(user)
```

SQLAlchemy sait qu'il devra être inséré dans la base.

### Persistent

Après un `flush()` ou un `commit()`.

```
session.commit()
```

L'objet existe maintenant dans la base de données.

### Detached

Si la session est fermée :

```
session.close()
```

ou :

```
with SessionLocal() as session:
    ...
```

L'objet devient détaché de la session.

Il existe toujours en mémoire mais SQLAlchemy ne peut plus charger automatiquement ses relations.

Pour débuter, il suffit surtout de retenir :

```
Création -> add() -> commit() -> objet enregistré
```

---

## 16.3 `flush()`

Avant de comprendre `commit()`, il est important de connaître `flush()`.

```
user = Users(
    username="Alice",
    email="alice@mail.com"
)

session.add(user)

session.flush()

print(user.id)
```

Après le `flush()`, PostgreSQL a déjà généré l'identifiant.

Par exemple :

```
1
```

Pourtant, la transaction n'est pas encore validée.

Différence :

```
session.flush()
```

* envoie les requêtes SQL à PostgreSQL ;

* récupère les valeurs générées ;

* ne valide pas la transaction.

  session.commit()

* effectue automatiquement un `flush()` ;

* valide définitivement la transaction.

Résumé :

```
flush()  -> envoyer
commit() -> envoyer + valider
```

---

## 16.4 Gérer les erreurs d'intégrité

La base de données peut refuser certaines opérations.

Exemple :

```
user = Users(
    username="Alice",
    email="alice@mail.com"
)

session.add(user)
session.commit()
```

Si un autre utilisateur possède déjà le même email ou le même username, PostgreSQL déclenchera une erreur.

SQLAlchemy remonte généralement cette erreur sous forme d'`IntegrityError`.

```
from sqlalchemy.exc import IntegrityError

try:
    session.add(user)
    session.commit()

except IntegrityError:
    session.rollback()
    print("Utilisateur déjà existant")
```

Important :

Après une erreur pendant un `commit()`, il faut généralement effectuer :

```
session.rollback()
```

avant de continuer à utiliser la session.

## 17. Read par nom

```python
def get_user_by_name(session: Session, username: str):
    stmt = select(Users).where(Users.username == username)

    return session.execute(stmt).scalar_one_or_none()
```

Cette fonction cherche un utilisateur par son `username`.

Si elle trouve un utilisateur, elle le retourne.

Si elle ne trouve rien, elle retourne `None`.

---

## 18. Read tous les utilisateurs

```python
def get_all_users(session: Session):
    stmt = select(Users)

    return session.execute(stmt).scalars().all()
```

Cette fonction retourne une liste d'utilisateurs.

Utilisation :

```python
with SessionLocal() as session:
    users = get_all_users(session)
    for user in users:
        print(user)
```

---

## 19. Read avec relation

Il y a deux choses importantes à distinguer :

- `join()` ajoute une jointure dans la requête SQL.
- `joinedload()` demande à SQLAlchemy de charger directement la relation dans les objets ORM.

Ces deux outils ne font pas exactement la même chose.

### Utiliser `join()`

```python
def get_by_id_with_profil(session: Session, id):
    stmt = select(Users).join(Users.profil).where(Users.id == id)

    return session.execute(stmt).scalar_one_or_none()
```

Ici, on utilise un `join`.

```python
join(Users.profil)
```

Cela permet de chercher un utilisateur qui a un profil associé.

Le `join()` est utilisé dans la requête SQL. Il sert ici à filtrer les utilisateurs pour garder seulement ceux qui ont un profil.

Par contre, le `join()` ne veut pas dire que la relation `user.profil` est déjà chargée dans l'objet Python retourné par l'ORM.

Si on accède ensuite à la relation :

```python
print(user.profil)
```

SQLAlchemy peut faire une requête SQL supplémentaire pour charger le profil. C'est le comportement de chargement paresseux, appelé lazy loading.

Équivalent SQL simplifié :

```sql
SELECT users.*
FROM users
JOIN profiles ON users.id = profiles.user_id
WHERE users.id = 1;
```

### Utiliser `joinedload()`

Si on veut que la relation soit directement chargée en mémoire avec l'utilisateur, on utilise `options(joinedload(...))`.

```python
from sqlalchemy.orm import joinedload

def get_by_id_with_profil_loaded(session: Session, id):
    stmt = (
        select(Users)
        .options(joinedload(Users.profil))
        .where(Users.id == id)
    )

    return session.execute(stmt).scalar_one_or_none()
```

Ici, SQLAlchemy retourne un objet `Users` avec sa relation `profil` déjà chargée.

Donc, quand on fait :

```python
print(user.profil)
```

SQLAlchemy n'a pas besoin de refaire une requête SQL uniquement pour récupérer le profil.

On peut aussi charger tous les utilisateurs avec leur profil :

```python
def get_all_users_with_profil(session: Session):
    stmt = (
        select(Users)
        .options(joinedload(Users.profil))
    )

    return session.execute(stmt).scalars().all()
```

Résumé :

- `join()` : utile pour construire la requête SQL, filtrer ou trier sur une relation.
- `joinedload()` : utile pour charger la relation dans les objets ORM dès la première requête.

---

## 20. Update

Exemple de fonction de modification :

```python
def update_user_email(session: Session, user_id: int, new_email: str):
    stmt = select(Users).where(Users.id == user_id)
    user = session.execute(stmt).scalar_one_or_none()

    if user is None:
        return None

    user.email = new_email
    session.commit()
    session.refresh(user)

    return user
```

Avec l'ORM, on modifie simplement les attributs Python.

```python
user.email = "new@mail.com"
```

Puis on valide :

```python
session.commit()
```

---

## 21. Delete

Exemple de suppression :

```python
def delete_user(session: Session, user_id: int):
    stmt = select(Users).where(Users.id == user_id)
    user = session.execute(stmt).scalar_one_or_none()

    if user is None:
        return False

    session.delete(user)
    session.commit()

    return True
```

Étapes :

1. On cherche l'utilisateur.
2. Si l'utilisateur n'existe pas, on retourne `False`.
3. Sinon, on le supprime avec `session.delete(user)`.
4. On valide avec `session.commit()`.

---

## 22. Transactions

Une transaction est un groupe d'opérations qui doivent être validées ensemble.

Exemple :

```python
try:
    session.add(user)
    session.add(profile)
    session.commit()
except Exception as e:
    session.rollback()
    print(f"Erreur : {e}")
```

Si tout se passe bien, `commit()` enregistre.

En cas d'erreur, `rollback()` annule toutes les opérations du groupe — comme si rien ne s'était passé.

Pour débuter, il faut surtout retenir :

- `commit()` valide ;
- `rollback()` annule ;
- sans `commit()`, les changements ne sont pas sauvegardés.

---

## 23. Exemple complet

```python
with SessionLocal() as session:
    user = create_user(
        session=session,
        username="Alice",
        email="alice@mail.com",
        country="Belgium"
    )

    profile = create_profil(
        user_id=user.id,
        bio="Développeuse Python",
        session=session
    )

    print(user)
    print(profile)
```

---

## 24. Structure du projet

```text
alchemy/
├── crud/
│   ├── profil_crud.py
│   └── user_crud.py
├── db/
│   └── database.py
├── models/
│   ├── profiles.py
│   └── users.py
├── main.py
├── readme.md
└── requirements.txt
```

Rôle des dossiers :

- `db/` : connexion à la base, engine, session, classe `Base`.
- `models/` : classes qui représentent les tables.
- `crud/` : fonctions pour créer, lire, modifier, supprimer.
- `main.py` : script de test et point d'entrée.

---

## 25. Bonnes pratiques pour débuter

- Utiliser `with SessionLocal() as session` pour fermer proprement la session.
- Ne pas mettre les mots de passe directement dans le code.
- Utiliser `.env` pour la configuration locale.
- Donner des noms clairs aux fonctions CRUD.
- Vérifier les cas où une requête retourne `None`.
- Activer `echo=True` pendant l'apprentissage pour voir le SQL généré.
- Garder les modèles dans `models/` et les fonctions de requête dans `crud/`.

---

## 26. Exercices proposés

1. Ajouter une fonction `get_user_by_id`.
2. Ajouter une fonction `update_user_country`.
3. Ajouter une fonction `delete_user`.
4. Afficher tous les utilisateurs avec leur profil.
5. Gérer le cas où un utilisateur n'a pas encore de profil.
6. Ajouter une table `posts` avec une relation one-to-many : un utilisateur peut avoir plusieurs posts.

---

## 27. Résumé

Les objets essentiels à retenir :

- `engine` : connexion entre SQLAlchemy et la base.
- `Base` : classe mère des modèles.
- `SessionLocal` : fabrique de sessions.
- `session` : objet de travail avec la base.
- `Mapped` et `mapped_column` : déclaration des colonnes.
- `relationship` : déclaration des relations entre modèles.
- `select()` : construction d'une requête.
- `stmt` : variable qui contient une requête.
- `session.execute(stmt)` : exécution de la requête.
- `commit()` : validation des changements.
- `refresh()` : recharge un objet depuis la base.
- `rollback()` : annulation d'une transaction en cas d'erreur.

## 28. Fonctions SQL avec `func()`

SQLAlchemy permet d'utiliser les fonctions SQL classiques grâce à `func`.

```
from sqlalchemy import func
```

### COUNT

Compter les utilisateurs :

```
stmt = select(func.count(Users.id))

total = session.execute(stmt).scalar_one()
```

Équivalent SQL :

```
SELECT COUNT(id)
FROM users;
```

### AVG

Prix moyen des jeux :

```
stmt = select(func.avg(Games.price))

average_price = session.execute(stmt).scalar_one()
```

### SUM

Total des heures jouées :

```
stmt = select(func.sum(UserGames.hours_played))

total_hours = session.execute(stmt).scalar_one()
```

### MAX

Jeu le plus cher :

```
stmt = select(func.max(Games.price))

max_price = session.execute(stmt).scalar_one()
```

### GROUP BY

Nombre d'utilisateurs par pays :

```
stmt = (
    select(
        Users.country,
        func.count(Users.id)
    )
    .group_by(Users.country)
)

results = session.execute(stmt).all()
```

Équivalent SQL :

```
SELECT country, COUNT(id)
FROM users
GROUP BY country;
```

Ces fonctions permettent de reproduire la majorité des requêtes SQL d'analyse directement avec SQLAlchemy ORM.
