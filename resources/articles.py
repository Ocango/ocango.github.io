from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required

from models.articles import ArticleModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('topic',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('picture_url',
                          type=str,
                          required=False,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('article_url',
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
_user_parser.add_argument('link_project',
                          type=int,
                          required=False,
                          help="This field cannot be blank."
                          )

class Article(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        data = _user_parser.parse_args()
        if ArticleModel.find_by_topic(data['topic']):
            return {'message': "文章名称 '{}' 已存在。".format(data['topic'])}, 400
        store = ArticleModel(data['topic'],data['picture_url'] if data['picture_url'] is not None else 'images/pic01.jpg',data['article_url'],data['introduce'],data['link_project'],data['weight'])
        try:
            store.save_to_db()
        except:
            return {"message": "后台数据处理发生异常，请联系网站管理员。"}, 500

        return {"message": "新建文章纲要成功！"}, 201