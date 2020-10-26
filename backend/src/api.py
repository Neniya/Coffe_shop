import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization')
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET,POST,PATCH,DELETE,OPTIONS')
    return response


'''
uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES
'''
endpoint GET /drinks
        contains only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
def get_drinks():
    try:
        drinks = list(map(Drink.short, Drink.query.all()))
        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200
    except Exception:
        abort(422)


'''
endpoint GET /drinks-detail
        requires the 'get:drinks-detail' permission
        contains the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth("get:drinks-detail")
def get_drinks_detail(token):
    try:
        drinks = list(map(Drink.long, Drink.query.all()))
        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200

    except Exception:
        abort(422)


'''
endpoint POST /drinks
        creates a new row in the drinks table
        requires the 'post:drinks' permission
        contains the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth("post:drinks")
def create_drink(token):
    try:
        if request.data:
            body = request.get_json()
            new_title = body.get('title')
            new_recipe = json.dumps(request.json['recipe'])
            new_drink = Drink(title=new_title, recipe=new_recipe)
            Drink.insert(new_drink)
            drinks = list(map(Drink.long, Drink.query.all()))
            return jsonify({
                "success": True,
                "drinks": drinks
            }), 200
            return jsonify(result)
    except Exception:
        abort(422)


'''
endpoint PATCH /drinks/<id>
        where <id> is the existing model id
        requires the 'patch:drinks' permission
        contains the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(token, drink_id):
    '''Updates drink by id'''
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        print(drink_id)
        # responds with a 404 error if <id> is not found
        if drink is None:
            abort(404)

        # update the corresponding row for <id>

        body = request.get_json()
        drink.title = body.get('title')
        drink.update()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200
    except Exception:
        abort(422)


'''
endpoint DELETE /drinks/<id>
        where <id> is the existing model id
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(token, drink_id):
    '''Delete drink by id'''
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        print(drink_id)
        # responds with a 404 error if <id> is not found
        if drink is None:
            abort(404)

        # deletes the corresponding row for <id>
        drink.delete()
        return jsonify({
            'success': True,
            'delete': drink_id
        })
    except Exception:
        abort(422)


# Error Handling
'''
error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
error handling for 404 resource not found
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
error handling for 401 Unauthorized
'''


@app.errorhandler(401)
def not_unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401


'''
error handler for AuthError
'''


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    """
    Receive the raised authorization error and propagates it as response
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
