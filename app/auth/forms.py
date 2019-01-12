from flask_wtf import FlaskForm
from app.models import User
from wtforms import StringField,BooleanField,PasswordField,SubmitField
from wtforms.validators import Required,EqualTo,Email,Length,Regexp
from wtforms import ValidationError



class RegisteForm(FlaskForm):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])
    name = StringField('Username',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',message='Username must be')])
    password = PasswordField('Password',validators=[\
            Required(),EqualTo('password2',message='password must be match')])
    password2 = PasswordField('Confirm Password',validators=[Required()])
    submit = SubmitField('Registe')

    def validate_email(self,field):
        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            raise ValidationError('Email already register')

    def validate_name(self,field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Username is already in use.')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])
    password = PasswordField('Password',validators=[Required()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('Log in')
