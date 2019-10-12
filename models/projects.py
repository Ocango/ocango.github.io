from db import db
from datetime import datetime
from models.articles import ArticleModel

class ProjectModel(db.Model):
    __tablename__='project'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    icon = db.Column(db.String(40))
    weight = db.Column(db.Integer,nullable=False)#权重,默认1,最大10，不实际卡控
    introduce = db.Column(db.String(1000))
    article_url = db.Column(db.Boolean,default=False,nullable=False)
    create_time = db.Column(db.DateTime , nullable=False , default=datetime.now)
    articles = db.relationship('ArticleModel', lazy='dynamic')

    def __init__(self, name, icon, introduce,article_url,weight = 1):
        self.name = name
        self.icon = icon
        self.weight = weight
        self.article_url = article_url
        self.introduce = introduce

    def json(self):
        store = ArticleModel.find_by_topic(self.name)
        return {
            "id":self.id,
            "name":self.name,
            "icon":self.icon,
            "introduce":self.introduce,
            "article_url":self.article_url,
            "article_id":store.id if store is not None else -1
        }

    def __repr__(self):
        return '<ProjectModel (name=%r,weight=%r,introduce=%r)>' % (self.name,self.weight,self.introduce)

    def get_all_article(self,maxindex = 3):
        '''获得关联article，默认最大值3'''
        return {
            'name':self.name,
            'id':self.id,
            'articles': [article.json() for article in (self.articles.limit(maxindex).all() if maxindex is not None else self.articles.all())]
        }
    #抓取展示目录，默认最大值4
    @classmethod
    def get_all_projects_bydict(cls,maxindex = 4):
        '''抓取展示目录，默认最大值4'''
        return [project.json() for project in (cls.query.order_by(cls.weight.desc()).limit(maxindex).all() if maxindex is not None else cls.query.order_by(cls.weight.desc()).all())]
    
    #查找重名
    @classmethod
    def find_by_name(cls, name):
        '''查找重名'''
        return cls.query.filter_by(name=name).first()
    #查找重名
    @classmethod
    def find_by_id(cls, id):
        '''查找重名'''
        return cls.query.filter_by(id=id).first()
    #当新增project时，新增关联article
    def insert_link_article(self):
        '''当新增project时，新增关联article'''
        store = ArticleModel.find_by_topic(self.name)
        if store:
            return False
        else:
            newarticle = ArticleModel(self.name,'images/pic01.jpg',False,self.introduce,self.id,1)
            newarticle.save_to_db()

    #project入库
    def save_to_db(self):
        '''project入库'''
        db.session.add(self)
        db.session.commit()
    
    # #临时取巧使用
    # @staticmethod
    # def add_project():
    #     project1 = ProjectModel('我的主站搭建','fa-newspaper-o','欢迎来到OcanGo的个人主站，本站点原生模板源自HTML5 UP，是一个Jquery的自适应模板。后加工基于Flask，服务器环境为centos+nginx+uwsgi。',10)
    #     project1.save_to_db()
    #     project2 = ProjectModel('流处理——由关键词屏蔽开始','fa-stack-overflow','',9)