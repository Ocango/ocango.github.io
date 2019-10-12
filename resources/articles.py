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
                          type=bool,
                          required=True,
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

    @classmethod
    @jwt_required
    def put(cls):
        data = _user_parser.parse_args()
        store = ArticleModel.find_by_topic(data['topic'])
        if store:
            if store.link_project == data['link_project']:
                store.picture_url = data['picture_url'] if data['picture_url'] is not None else 'images/pic01.jpg'
                store.introduce = data['introduce'] if data['introduce'] is not None else store.introduce
                store.article_url = data['article_url'] if data['article_url'] is not None else store.article_url
                store.weight = data['weight'] if data['weight'] is not None else store.weight
            else:
                return {"message": "禁止修改对应的专题链接。"}, 400
        else:
            store = ArticleModel(data['topic'],data['picture_url'] if data['picture_url'] is not None else 'images/pic01.jpg',data['article_url'],data['introduce'],data['link_project'],data['weight'])
        try:
            store.save_to_db()
        except:
            return {"message": "后台数据处理发生异常，请联系网站管理员。"}, 500

        return {"store":store.json(),"message": "更新/新增项目状态成功！"}, 201