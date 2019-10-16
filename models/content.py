from db import db
from datetime import datetime

class ContentModel(db.Model):
    __tablename__='content'

    id = db.Column(db.Integer, primary_key=True)
    content_md = db.Column(db.String(5000))
    content_HTML = db.Column(db.String(5000))
    create_time = db.Column(db.DateTime , nullable=False , default=datetime.now)

    def __init__(self,id,content_md,content_HTML):
        self.content_md = content_md
        self.content_HTML = content_HTML
        self.id = id
    
    def json(self):
        return {
            "id":self.id,
            "content_HTML":self.content_HTML
        }

    #查找重号
    @classmethod
    def find_by_id(cls, id):
        '''查找重号,获取id对应资料'''
        return cls.query.filter_by(id=id).first()


    #content入库
    def save_to_db(self):
        '''content入库,记得一定要验证article存在性，此处不做验证'''
        db.session.add(self)
        db.session.commit()