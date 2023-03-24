from flask_restful import Resource
from .. import api, db
from models import User
from flask_login import current_user

class UserAPI(Resource):
    def get(self, user_id):
        # user = User.query.get_or_404(user_id)
        
        return {"working" : "ok"}

    def put(self, username):
        print("PUT username", username)
        return {"username": username}, 200
    
    def delete(self, username):
        print("DELETE user", username)
        return {"username": username}, 200
    
    def post(self, username):
        print("POST user", username)
        return {"username": username}, 200

api.add_resource(UserAPI, "api/user") 