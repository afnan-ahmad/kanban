from flask_restful import Resource
from flask_security import auth_required, current_user


class UserAPI(Resource):
    @auth_required('token')
    def get(self):
        return {
            'displayName': current_user.name
        }
