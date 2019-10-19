from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required

from models.content import ContentModel
from models.articles import ArticleModel
import main_parse

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('id',
                          type=int,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('content_md',
                          type=str,
                          required=False,
                          help="This field cannot be blank."
                          )


class Content(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        '''上传md数据，并进行转档，转化为html'''
        data = _user_parser.parse_args()
        article = ArticleModel.find_by_id(data['id'])
        if article:
            if ContentModel.find_by_id(data['id']):
                return {'message': "文章ID '{}' 详细资料已存在，如需更新请使用put请求。".format(data['id'])}, 400
            else:
                my_content = ContentModel(data['id'],data['content_md'],'')
                main_parse.exe_mdToHTML(my_content)
                try:
                    my_content.save_to_db(article)
                    return {"my_content":my_content.json(),"message": "更新/新增项目状态成功！"}, 201
                except:
                    return {"message": "后台数据处理发生异常，请联系网站管理员。"}, 500
        else:
            return {'message': "文章ID '{}' 不存在，请优先新建文章。".format(data['id'])}, 400
        
        



    @classmethod
    @jwt_required
    def put(cls):
        '''更新或新增md数据并转化'''
        data = _user_parser.parse_args()
        article = ArticleModel.find_by_id(data['id'])
        if article:
            my_content = ContentModel.find_by_id(data['id'])
            if my_content:
                my_content.content_md = data['content_md']
            else:
                my_content = ContentModel(data['id'],data['content_md'],'')

            main_parse.exe_mdToHTML(my_content)
            try:
                my_content.save_to_db(article)
            except:
                return {"message": "后台数据处理发生异常，请联系网站管理员。"}, 500
        else:
            return {'message': "文章ID '{}' 不存在，请优先新建文章。".format(data['id'])}, 400
        
        return {"my_content":my_content.json(),"message": "更新/新增项目状态成功！"}, 201
