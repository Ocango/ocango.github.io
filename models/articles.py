from db import db
from datetime import datetime
from models.projects import ProjectModel

class ArticleModel(db.Model):
    __tablename__='article'

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(80))
    picture_url = db.Column(db.String(80))
    article_url = db.Column(db.Boolean,default=False,nullable=False)
    weight = db.Column(db.Integer,nullable=False)#权重,默认1,最大10，不实际卡控
    introduce = db.Column(db.String(1000))
    link_project = db.Column(db.Integer, db.ForeignKey('project.id'))
    create_time = db.Column(db.DateTime , nullable=False , default=datetime.now)

    store = db.relationship('ProjectModel')

    def __init__(self, topic, picture_url, article_url,introduce,link_project,weight = 1):
        self.topic = topic
        self.picture_url = picture_url
        self.article_url = article_url
        self.introduce = introduce
        self.link_project = link_project
        self.weight = weight
    
    def json(self):
        return {
            "id":self.id,
            "topic":self.topic,
            "picture_url":self.picture_url,
            "article_url":self.article_url,
            "introduce":self.introduce,
            "link_project":self.link_project,
            "data_str":self.create_time.strftime('%Y-%m-%d')
        }
    
    def __repr__(self):
        return '<ArticleModel (topic=%r,introduce=%r,link_project=%r)>' % (self.topic,self.introduce,self.link_project)
    
    #抓取sidebar目录,全部
    @classmethod
    def get_all_acricles_bytree(cls,whereitem,wherestr):
        '''抓取sidebar目录,全部'''
        if whereitem == 'link_project':
            return [
                {
                    "project_name":project.name,
                    "link_articles":[
                        article.json() for article in project.articles
                        ]
                } for project in ProjectModel.query.filter_by(id = wherestr).all()
            ]
        elif whereitem == 'link_date':
            return [
                {
                    "project_name":project.name,
                    "link_articles":[
                        article.json() for article in project.articles.filter(db.and_(db.extract('month', ArticleModel.create_time) == wherestr[5:7],db.extract('year', ArticleModel.create_time) == wherestr[:4])).all()
                        ]
                } for project in ProjectModel.query.all()
            ]
        else:
            print(whereitem)
            return [
                {
                    "project_name":project.name,
                    "link_articles":[
                        article.json() for article in project.articles.filter(db.or_(ArticleModel.topic.like('%'+wherestr+'%'),ArticleModel.introduce.like('%'+wherestr+'%'))).all()
                        ]
                } for project in ProjectModel.query.all()
            ]            

    #抓取展示目录，默认最大值4
    @classmethod
    def get_all_acricles_bydict(cls,maxindex = 6):
        '''抓取展示目录，默认最大值6'''
        return [article.json() for article in (cls.query.order_by(cls.weight.desc()).limit(maxindex).all() if maxindex is not None else cls.query.order_by(cls.weight.desc()).all())]

    #查找重名
    @classmethod
    def find_by_topic(cls, topic):
        '''查找重名'''
        return cls.query.filter_by(topic=topic).first()
    #查找，依据id
    @classmethod
    def find_by_id(cls,id):
        '''查找，依据id'''
        return cls.query.filter_by(id=id).first()
    #article入库
    def save_to_db(self):
        '''article入库'''
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def insert_link_article(cls,project_obj):
        '''当新增project时，新增关联article'''
        store = cls.find_by_topic(project_obj.name)
        if store:
            return False
        else:
            newarticle = ArticleModel(project_obj.name,'images/pic01.jpg',False,project_obj.introduce,project_obj.id,1)
            newarticle.save_to_db()