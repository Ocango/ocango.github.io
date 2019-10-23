from datetime import timedelta

from flask import Flask, jsonify, render_template,abort
from flask_jwt_extended import JWTManager
from flask_restful import Api

import main_parse
from db import db
from models.projects import ProjectModel
from resources.projects import Project
from models.articles import ArticleModel
from models.content import ContentModel
from resources.user import UserLogin, UserRegister,TokenRefresh
from resources.articles import Article
from resources.content import Content
from models.feature import FeatureModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)
db.init_app(app)

#API管理，加入认证机制
#可以用os.urandom(24)生成随机的密钥
app.config['JWT_SECRET_KEY'] = b"\x8e\xaes\x01\xb7'p\xa81\xb7\x92\xca\xc5\x1a9^\xa3\x18\xb3\rOx<x"  # 也可以使用 app.secret 就像之前一样
ACCESS_EXPIRES = timedelta(minutes=15)
REFRESH_EXPIRES = timedelta(days=30)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = REFRESH_EXPIRES
# app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens
jwt = JWTManager(app)


# 全文处理，包括错误处理和预处理等

@app.before_first_request
def create_tables():
    db.create_all()

@app.errorhandler(404)
def page_not_found(e):
    # 页面未找到
    return render_template('errorpage/404.html'), 404

# 用户认证
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:   # instead of hard-coding, we should read from a config file to get a list of admins instead
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': '此令牌已失效。',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'message': '签名认证失败。',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "请求不包含认证令牌。",
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "需要新令牌。",
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "令牌已被撤销.",
        'error': 'token_revoked'
    }), 401



# 连接地址
@app.route('/')
def index():
    return render_template(
        'index.html',
        now_time=main_parse.welcome_home(),
        projects=ProjectModel.get_all_projects_bydict(),
        articles=ArticleModel.get_all_acricles_bydict(),
        sidebar_project = ProjectModel.get_all_projects_bytree()
    )

@app.route('/elements')
def elements():
    return render_template('elements_copy.html',sidebar_project = ProjectModel.get_all_projects_bytree())

# @app.route('/generic')
# def generic():
#     return render_template('generic.html')

@app.route('/article/<int:topic>')
def articles(topic):
    article = ArticleModel.find_by_id(topic)
    if article:
        project = ProjectModel.find_by_id(article.link_project)
        articles_list = project.get_all_article(None)
        content = ContentModel.find_by_id(article.id)
        if content:
            article_content = content.content_HTML
        else:
            article_content = None
    else:
        abort(404)
    return render_template(
        'generic.html',
        article_id = topic,
        articles = {
            "articles_len" : len(articles_list['articles']),
            "articles":articles_list['articles'],
            "article_content":article_content,
            "article_name":article.topic},
        sidebar_project = ProjectModel.get_all_projects_bytree()
        )

@app.route('/query_item/<string:whereitem>/<string:wherestr>')
def query_item(whereitem,wherestr):
    sidebar_article = ArticleModel.get_all_acricles_bytree(whereitem,wherestr)
    sidebar_feature = FeatureModel.get_all_feature_bytree(whereitem,wherestr)
    count_article = sum(len(link['link_articles']) for link in sidebar_article)
    count_feature = sum(len(link['link_features']) for link in sidebar_feature)
    print(sidebar_article,sidebar_feature)
    return render_template(
        'elements.html',
        whereitem = main_parse.querystr(whereitem,wherestr),
        sidebar_article = sidebar_article,
        sidebar_feature = sidebar_feature,
        count_article = count_article,
        count_feature = count_feature,
        sidebar_project = ProjectModel.get_all_projects_bytree()
    )

api.add_resource(Project,'/api/project')
# api.add_resource(UserRegister, '/api/register')#临时创建管理员用户，安保级别较高的请求需要JWT认证，所以注解不允许再创建用户，其实也可以用设定管理员的方式通过add_claims_to_jwt验证，但是懒~··~
api.add_resource(UserLogin, '/api/login')
api.add_resource(Article,'/api/article')
api.add_resource(TokenRefresh, '/api/refresh')#刷新令牌机制
api.add_resource(Content, '/api/content')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
