from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,#创建认证TOKEN
    create_refresh_token,#创建刷新TOKEN
    jwt_refresh_token_required,#需要刷新TOKEN
    get_jwt_identity,#获取TOKEN的identity
    get_raw_jwt,#令牌注销机制
    jwt_required#用JWT保护端点
)
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "用户名称已存在。"}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "用户创建成功."}, 201


class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200

        return {"message": "Invalid Credentials!"}, 401


# class UserLogout(Resource):
#     @jwt_required
#     def post(self):
#         jti = get_raw_jwt()['jti']
#         BLACKLIST.add(jti)
#         return {"message": "Successfully logged out"}, 200


# class User(Resource):
#     """
#     This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
#     sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
#     """
#     @classmethod
#     def get(cls, user_id: int):
#         user = UserModel.find_by_id(user_id)
#         if not user:
#             return {'message': 'User Not Found'}, 404
#         return user.json(), 200

#     @classmethod
#     def delete(cls, user_id: int):
#         user = UserModel.find_by_id(user_id)
#         if not user:
#             return {'message': 'User Not Found'}, 404
#         user.delete_from_db()
#         return {'message': 'User deleted.'}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
