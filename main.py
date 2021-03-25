from flask import jsonify, request 
from flask_pymongo import pymongo
from app import create_app
from bson.json_util import dumps
import db_config as db

app = create_app()

@app.route ('/test/')
def test():
    return jsonify({
"message":  "Cette API travail bien."
    })

@app.route('/admin/users/token', methods=['GET'])
#implementar que solo el master pueda acceder a esta ruta
def show_users():
    all_users = list(db.db.users.find())
    for users in all_users:
       del users ["_id"]
    return jsonify({"all_users":all_users})
    


@app.route('/users/<int:n_top>/', methods=['GET'])
def show_a_top_users(n_top):
    user = db.db.users.find_one({'n_top':n_top})
    del user ["_id"]

    return jsonify({
            "user":user
        })


@app.route('/api/new_user/', methods=['POST'])
def add_new_users():
    db.db.users.insert_one({
        "n_top": request.json["n_top"],
        "name":request.json["name"],
        "email":request.json["email"],
        "phone":request.json["phone"],
        "password":request.json["password"]       
    })
    return jsonify({
        "message":"Se añadio correctamente un nuevo usuario",
        "status": 200,
    })


@app.route('/api/top_users/update/<int:n_top>',methods=['PUT'])
def update_users(n_top):

    if db.db.users.find_one({'n_top':n_top}):
        db.db.users.update_one({'n_top':n_top},
        {'$set':{   
        "n_top": request.json["n_top"],
        "name":request.json["name"],
        "email":request.json["email"],
        "email":request.json["email"],
        "password":request.json["password"]
        }})
    else:
        return jsonify({"status":400, "message": f"the user #{n_top} not found"})

    return jsonify({"status":200, "message": f"The user #{n_top} has been updated successfully"})


@app.route('/api/top_users/del/<int:n_top>',methods=['DELETE'])
def delete_users(n_top):
    if db.db.users.find_one({'n_top':n_top}):
        db.db.users.delete_one({'n_top':n_top})
    else:
        return jsonify({"status":400, "message": f"the user #{n_top} not found"})
    return jsonify({"status":200, "message": f"The user #{n_top} has been deleted successfully"})

if __name__ == '__main__':
    app.run(load_dotenv=True, port=8080) 