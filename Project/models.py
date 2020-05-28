from Project import db
from datetime import datetime

class Articles(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer,primary_key=True)
    author = db.Column(db.Text)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    source = db.Column(db.Text)
    url = db.Column(db.Text)
    url_to_image = db.Column(db.Text)
    summary = db.Column(db.Text)
    published_date = db.Column(db.DateTime,default = datetime.utcnow)
    sentiment = db.Column(db.String(20))
    probability = db.Column(db.String(20))
    article_type = db.Column(db.String(20))