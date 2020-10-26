# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
   


## **API**
API is represented in `./src/api.py`

## Error handling
Errors are returned as JSON objects in the following format:
`{
"success": False,
"error": 404,
"message": "resource not found"
}`

The API will return five error types when requests fail:
* 400: Best Request
* 404: Resouses not found
* 422: Not Processable
* 401: Unauthorized
* 403: Forbidden

## Endpoints

* [GET '/drinks'](#get-drinks)
* [GET '/drinks-detail](#get-drinks-detail)
* [POST '/drinks'](#post-questions)
* [PATCH '/drinks/&lt;nt:drink_id&gt;'](#patch-drinksintdrink_id)
* [DELETE '/drinks/&lt;nt:drink_id&gt;'](#delete-drinksintdrink_id)


### GET '/drinks'

* General:
    * Fetches a dictionary of drinks objects. 
    * Request Arguments: None
    * Returns: Status code 200, success value and  a list of drinks objects 

* Sample in Postman(for role "Manager"): GET `{{host}}/drinks`

```
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "parts": 3
                },
                {
                    "color": "red",
                    "parts": 1
                }
            ],
            "title": "Cherry water"
        },
        {
            "id": 2,
            "recipe": [
                {
                    "color": "blue",
                    "parts": 1
                }
            ],
            "title": "water"
        },
        {
            "id": 3,
            "recipe": [
                {
                    "color": "brown",
                    "parts": 1
                },
                {
                    "color": "blue",
                    "parts": 3
                },
                {
                    "color": "white",
                    "parts": 1
                }
            ],
            "title": "Tee"
        }
    ],
    "success": true
}
```


### GET '/drinks-detail'
* General:
    * Fetches a dictionary of drinks objects. 
    * Request Arguments: None
    * Returns: Status code 200, success value and  a list of drinks objects 

* Sample in Postman(for role "Manager"): GET `{{host}}/drinks-detail`

```
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 3
                },
                {
                    "color": "red",
                    "name": "cherry syrup",
                    "parts": 1
                }
            ],
            "title": "Cherry water"
        },
        {
            "id": 2,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                }
            ],
            "title": "water"
        },
        {
            "id": 3,
            "recipe": [
                {
                    "color": "brown",
                    "name": "Tee",
                    "parts": 1
                },
                {
                    "color": "blue",
                    "name": "Hot water",
                    "parts": 3
                },
                {
                    "color": "white",
                    "name": "Sugar",
                    "parts": 1
                }
            ],
            "title": "Tee"
        }
    ],
    "success": true
}
```

### POST '/drinks'

* General:
    * creates a new row in the drinks table. 
    * Request Arguments: None
    * Returns: Status code 200, success value and  an array containing only the newly created drink

* Sample in Postman(for role "Manager"): POST `{{host}}/drinks`
```
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "Water",
                    "parts": 1
                }
            ],
            "title": "Water3"
        }
    ],
    "success": true
}
```


### PATCH '/drinks/<int:drink_id>'
* General:
    * Updates the question of the given ID if it exists.. 
    * Request Arguments: drink_id
    * Returns: Status code 200, success value and an array containing only the updated drink 

* Sample in Postman(for role "Manager"): PATCH `{{host}}/drinks/1`

```
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "Water",
                    "parts": 1
                }
            ],
            "title": "Water5"
        }
    ],
    "success": true
}
```


### DELETE '/drinks/<int:drink_id>'
* General:
    * Deletes the question of the given ID if it exists.. 
    * Request Arguments: drink_id
    * Returns: Status code 200, success value and an id of the deleted record 

* Sample in Postman(for role "Manager"): DELETE `{{host}}/drinks/1`

```
{
    "delete": "1",
    "success": true
}
```
