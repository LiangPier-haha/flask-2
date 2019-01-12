from . import db,login_manager
from flask import current_app
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,unique=True)
    users = db.relationship('User',backref='role',lazy='dynamic')

    def __repr__(self):

        return '<Role %r>'% self.name


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String,unique=True)
    name = db.Column(db.String,unique=True)
    password_hash = db.Column(db.String)
    confirm = db.Column(db.Boolean,default=False)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>'% self.name


    @property
    def password(self):
        raise AttributeError('password is unreadly')
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def generate_registe_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])

        return s.dumps({'confirm':self.id})

    def confirmed(sef,token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm')!=self.id:
            return False
        self.confirm = True
        db.session.add(self)
        return True


#class AnonymousUser()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
