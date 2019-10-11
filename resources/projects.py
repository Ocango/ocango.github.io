from flask_restful import Resource,reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional

from models.projects import ProjectModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('name',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('icon',
                          type=str,
                          required=False,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('weight',
                          type=int,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('introduce',
                          type=str,
                          required=False,
                          help="This field cannot be blank."
                          )

class Project(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        data = _user_parser.parse_args()
        if ProjectModel.find_by_name(data['name']):
            return {'message': "项目名称 '{}' 已存在。".format(data['name'])}, 400

        store = ProjectModel(data['name'],data['icon'] if data['icon'] is not None else 'fa-newspaper-o',data['introduce'],data['weight'])
        try:
            store.save_to_db()
        except:
            return {"message": "后台数据处理发生异常，请联系网站管理员。"}, 500

        return {"message": "新建项目成功！"}, 201
    