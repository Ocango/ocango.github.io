from db import db
from datetime import datetime

class ProjectModel(db.Model):
    __tablename__='project'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    icon = db.Column(db.String(40))
    weight = db.Column(db.Integer,nullable=False)#权重,默认1,最大10，不实际卡控
    introduce = db.Column(db.String(1000))
    create_time = db.Column(db.DateTime , nullable=False , default=datetime.now)
    articles = db.relationship('ArticleModel', lazy='dynamic')

    def __init__(self, name, icon, introduce,weight = 1):
        self.name = name
        self.icon = icon
        self.weight = weight
        self.introduce = introduce

    def json(self):
        return {
            "name":self.name,
            "icon":self.icon,
            "introduce":self.introduce
        }

    def __repr__(self):
        return '<ProjectModel (name=%r,weight=%r,introduce=%r)>' % (self.name,self.weight,self.introduce)

    #抓取展示目录，默认最大值4
    @classmethod
    def get_all_projects_bydict(cls,maxindex = 4):
        '''抓取展示目录，默认最大值4'''
        return [project.json() for project in cls.query.order_by(cls.weight.desc()).limit(maxindex).all()]
    
    #查找重名
    @classmethod
    def find_by_name(cls, name):
        '''查找重名'''
        return cls.query.filter_by(name=name).first()
    
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