from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Lemonade, contact_schema, contacts_schema



api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}
    
@api.route('/lemonades', methods = ['POST'])
@token_required
def create_lemonade(current_user_token):
    time_to_make = request.json['time_to_make']
    color = request.json['color']
    num_of_lemons = request.json['num_of_lemons']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    lemonade = Lemonade(time_to_make, color, num_of_lemons, user_token=user_token)

    db.session.add(lemonade)
    db.session.commit()

    response = contact_schema.dump(lemonade)
    return jsonify(response) 

@api.route('/lemonades', methods = ['GET'])
@token_required
def get_lemonade(current_user_token):
    a_user = current_user_token.token
    lemonade = Lemonade.query.filter_by(user_token = a_user).all()
    response = contacts_schema.dump(lemonade)
    return jsonify(response)

@api.route('/lemonades/<id>', methods = ['GET'])
@token_required
def get_single_lemonade(current_user_token, id):
    lemonade = Lemonade.query.get(id)
    response = contact_schema.dump(lemonade)
    return jsonify(response)

@api.route('/lemonades/<id>', methods = ['POST', 'PUT'])
@token_required
def update_lemonade(current_user_token, id):
    lemonade = Lemonade.query.get(id)
    lemonade.time_to_make = request.json['time_to_make']
    lemonade.color = request.json['color']
    lemonade.num_of_lemons = request.json['num_of_lemons']
    lemonade.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(lemonade)
    return jsonify(response)

@api.route('/lemonades/<id>', methods = ['DELETE'])
@token_required
def delete_lemonade(current_user_token, id):
    lemonade = Lemonade.query.get(id)
    db.session.delete(lemonade)
    db.session.commit()
    response = contact_schema.dump(lemonade)
    return jsonify(response)