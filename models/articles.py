from db import db
from datetime import datetime

class ArticleModel(db.Model):
    __tablename__='article'

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(80))
    picture_url = db.Column(db.String(80))
    article_url = db.Column(db.String(80))
    weight = db.Column(db.Integer,nullable=False)#权重,默认1,最大10，不实际卡控
    introduce = db.Column(db.String(1000))
    link_project = db.Column(db.Integer, db.ForeignKey('project.id'))
    create_time = db.Column(db.DateTime , nullable=False , default=datetime.now)

    def __init__(self, topic, picture_url, article_url,introduce,link_project,weight = 1):
        self.topic = topic
        self.picture_url = picture_url
        self.article_url = article_url
        self.introduce = introduce
        self.link_project = link_project
        self.weight = weight
    
    def json(self):
        return {
            "topic":self.topic,
            "picture_url":self.picture_url,
            "article_url":self.article_url,
            "introduce":self.introduce
        }
    
    def __repr__(self):
        return '<ArticleModel (topic=%r,introduce=%r,link_project=%r)>' % (self.topic,self.introduce,self.link_project)
    
    #抓取展示目录，默认最大值4
    @classmethod
    def get_all_acricles_bydict(cls,maxindex = 6):
        '''抓取展示目录，默认最大值6'''
        return [article.json() for article in cls.query.order_by(cls.weight.desc()).limit(maxindex).all()]

    #查找重名
    @classmethod
    def find_by_topic(cls, topic):
        '''查找重名'''
        return cls.query.filter_by(topic=topic).first()
    
    #project入库
    def save_to_db(self):
        '''project入库'''
        db.session.add(self)
        db.session.commit()