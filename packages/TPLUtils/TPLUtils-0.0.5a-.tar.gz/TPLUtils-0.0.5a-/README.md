
# TPL Utils Package Documentation

This documentation provides an overview of the TPL package, which contains modules for database operations, test helpers, and utility functions. The package is organized into the following directories:

- `db`: Contains classes and methods related to database operations.
- `test`: Contains helper methods for testing.
- `utility`: Contains utility functions for logging, security, and other general-purpose tasks.

To run test use: `pytest -s -p no:warnings --cov=src`
## Table of Contents

1. [Database (db)](#database-db)
2. [Test Helpers (test)](#test-helpers-test)
3. [Utilities (utility)](#utilities-utility)

## Database (db)

The `db` directory contains classes and methods for database operations, such as connecting to a database, querying data, and managing transactions. Here's a brief overview of the main components:

- **config.py:** Firebase initialization and global database instance.
- **user.py:** User class definition, database operations for creating, retrieving, and updating user data.
- **website.py:** Website and related classes definition, database operations for creating, retrieving, updating, and deleting website data.

### config.py

This file is responsible for initializing the Firebase connection and providing a global database instance. The `db` variable is used throughout the other modules in the `db` directory to interact with the Firebase Firestore.

**Example import:**
```python
from src.TPL.db.config import db
```

### user.py

This file defines the User class, which represents a user in the system. The class includes methods for creating new users, saving user data, and retrieving user information by user ID or username. The User class also contains the following fields:

- user_id
- username
- allowed_deployments
- created_at
- updated_at
- fname
- lname
- email
- github
- linkedin
- phone
- photo_url
- role
- websites

**Methods**:

- `create(user_data: dict) -> 'User':` Creates a new user using the given user data and saves it to the database. Returns the created user instance.
- `save() -> None:` Saves the current user instance to the database.
- `get(user_id: str) -> 'User':` Retrieves a user by their user ID from the database. Raises an HTTPException with a 404 status code if the user is not found.
- `get_from_username(username: str) -> 'User':` Retrieves a user by their username from the database. Raises an HTTPException with a 404 status code if the user is not found.

**Example import**:

```python
from src.TPL.db.user import User
```

### website.py

This file defines the `Website`, `NewVariable`, `NewWebsite`, and `WebsiteType` classes. The `Website` class represents a website in the system and includes methods for creating, saving, retrieving, updating, and deleting website data. The Website class contains the following fields:

- website_id
- owner_id
- created_at
- updated_at
- deployed_at
- name
- description
- profile_image
- profile_logo
- env
- port_number
- repo_url
- template
- path

**Methods** :

- `save():` Saves the current website instance to the database.
to_dict(): Returns a dictionary representation of the website instance, excluding the env field.
- `delete():` Deletes the current website instance from the database.
- `create(website_data: dict) -> 'Website':` Creates a new website using the given website data and saves it to the database. Returns the created website instance.
- `get_from_id(website_id: str):` Retrieves a website by its ID from the database. Raises an HTTPException with a 404 status code if the website is not found.
- `get_from_user(website_name: str, user_id: str):` Retrieves a website by its name and user ID from the database. Raises an HTTPException with a 404 status code if the website is not found.

**Example import**:

```python
from src.TPL.db.website import Website, NewVariable, NewWebsite, WebsiteType
```

The `NewVariable` and `NewWebsite` classes are used for creating new website instances with the required fields. The `WebsiteType` enum class represents the website types, which are `frontend` and `backend`.


## Test Helpers (test)

The `test` directory contains helper methods for testing. These methods can be used to simplify test setup, execution, and teardown. Here's a brief overview of the main components:

- **get_token.py:** Generates a test user ID token for Firebase authentication.

### get_token.py

This file contains the `get_test_user_id_token` function, which generates a test user ID token for Firebase authentication. This token can be used in test cases that require an authenticated user.

**Methods:**

- `get_test_user_id_token(user_id: str = os.environ.get("TESTBOT_ID")) -> str`: Generates a test user ID token for the given user ID (or the default "TESTBOT_ID" environment variable). The function first creates a custom token using the Firebase Admin SDK, then exchanges it for an ID token using the Pyrebase library.

**Example import:**
```python
from src.TPL.test.get_token import get_test_user_id_token
```

## Utility (utility)

The `utility` directory contains various helper functions and classes for tasks such as logging, security, and other miscellaneous functions. Here's a brief overview of the main components:

- **logging.py:** Logger configuration and global logger instance.
- **security.py:** Firebase authentication, user verification, and admin verification.

### logging.py

This file sets up the global logger configuration and provides a `logger` instance that can be used throughout the application for logging purposes.

**Example import:**
```python
from src.TPL.utility.logging import logger
```

### security.py
This file contains functions for Firebase authentication, user verification, and admin verification. It defines the DecodedToken class, which represents a decoded Firebase authentication token, as well as the verify_user and verify_admin functions.

**Methods:**

- `DecodedToken.get(decoded_token: dict) -> DecodedToken:` Creates a new DecodedToken instance from the given decoded token dictionary.
- `verify_user(bearer: str = Depends(http_bearer)) -> DecodedToken:` Verifies the provided access token and returns a DecodedToken instance if the token is valid. Raises an HTTPException with a 401 status code if the token is invalid.
- `verify_admin(bearer: str = Depends(http_bearer)) -> DecodedToken:` Verifies the provided access token, checks if the user is an admin, and returns a DecodedToken instance if the token is valid and the user is an admin. Raises an HTTPException with a 401 status code if the token is invalid or the user is not an admin.

**Example import:**
```python
from src.TPL.utility.security import verify_user, verify_admin, DecodedToken
```

