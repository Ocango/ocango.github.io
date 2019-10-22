from db import db
from datetime import datetime
from models.projects import ProjectModel

class FeatureModel(db.Model):
    __tablename__='feature'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    weight = db.Column(db.Integer,nullable=False)#权重,默认1,最大10，不实际卡控
    introduce = db.Column(db.String(1000))
    link_project = db.Column(db.Integer, db.ForeignKey('project.id'))
    create_time = db.Column(db.DateTime , nullable=False , default=datetime.now)

    store = db.relationship('ProjectModel')

    def __init__(self, name, introduce,link_project,weight = 1):
        self.name = name
        self.introduce = introduce
        self.link_project = link_project
        self.weight = weight
    
    def json(self):
        return {
            "id":self.id,
            "name":self.name,
            "introduce":self.introduce,
            "link_project":self.link_project
        }
    
    def __repr__(self):
        return '<FeatureModel (name=%r,introduce=%r,link_project=%r)>' % (self.name,self.introduce,self.link_project)
    
    #抓取sidebar目录,全部
    @classmethod
    def get_all_feature_bytree(cls):
        '''抓取展示目录，全部'''
        return [
            {
                "project_name":project.name,
                "link_features":[
                    feature.json() for feature in project.features
                    ]
            } for project in ProjectModel.query.all()
        ]

    #查找重名
    @classmethod
    def find_by_name(cls, name):
        '''查找重名'''
        return cls.query.filter_by(name=name).first()
    #查找，依据id
    @classmethod
    def find_by_id(cls,id):
        '''查找，依据id'''
        return cls.query.filter_by(id=id).first()
    #feature入库
    def save_to_db(self):
        '''article入库'''
        db.session.add(self)
        db.session.commit()