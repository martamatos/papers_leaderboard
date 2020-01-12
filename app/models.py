from datetime import datetime
from hashlib import md5
from app import current_app, db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
import jwt
import enum


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))

    #papers_read = db.relationship('Comment', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')
    #ratings = db.relationship('Comment', back_populates='user')

    def __repr__(self):
        return f'User {self.name}'

    def __str__(self):
        return f'User {self.name}'

    def __hash__(self):
        return hash(self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    def get_n_papers_read(self):
        return str(len(self.comments))

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Paper(db.Model):
    __tablename__ = 'paper'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doi = db.Column(db.String(140), nullable=False)
    title = db.Column(db.String(140), nullable=False)
    first_author = db.Column(db.String(140), nullable=True)
    last_author = db.Column(db.String(140), nullable=True)
    paper_rating = db.Column(db.Integer)
    n_votes = db.Column(db.Integer)

    comments = db.relationship('Comment', back_populates='paper')
    #read_by_users = db.relationship('Comment', back_populates='paper')

    def __repr__(self):
        return f'{self.title}. {self.first_author}, {self.last_author}. {self.doi}'

    def __str__(self):
        return f'{self.title}. {self.first_author}, {self.last_author}. {self.doi}'

    def __hash__(self):
        return hash(self.title)

    def get_read_by_n_users(self):
        return str(len(self.comments))


class Comment(db.Model):
    __tablename__ = 'comment'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    paper_id = db.Column(db.Integer, db.ForeignKey('paper.id'), primary_key=True, nullable=False)
    text = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', back_populates='comments')
    paper = db.relationship('Paper', back_populates='comments')

    def __repr__(self):
        return f'{self.paper.title}.\n {self.user.name}.\n {self.rating}.\n {self.text}'

    def __str__(self):
        return f'{self.paper.title}.\n {self.user.name}.\n {self.rating}.\n {self.text}'


