from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Model for users"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String,
                           nullable=False)

    last_name = db.Column(db.String,
                          nullable=False)

    img_url = db.Column(db.String,
                        nullable=False,
                        default='https://media.istockphoto.com/vectors/missing-image-of-a-person-placeholder-vector-id1288129985?k=20&m=1288129985&s=612x612&w=0&h=OHfZHfKj0oqIDMl5f_oRqH13MHiB63nUmySYILbWbjE=')

    def __repr__(self):
        u = self
        return f"<User id={u.id} first name={u.first_name} last name={u.last_name} img={u.image_url}>"


class Post(db.Model):
    """Model for posts"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String, nullable=False)

    content = db.Column(db.String)

    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref="posts")
