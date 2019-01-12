from .forms import RegisteForm,LoginForm
from app.models import User
from app.emails import send_email
from flask import render_template,redirect,flash,url_for,request
from flask_login import login_required,current_user,login_user,logout_user
from . import auth
from app import db

@auth.before_app_request
def before_request():
    print( request.endpoint[:5])
    if current_user.is_authenticated and not current_user.confirm \
            and request.endpoint and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':

        print('11111111111111111')
        return redirect(url_for('auth.unconfirm'))
@auth.route('/unconfirm')
def unconfirm():
    print(22222222222222222)
    if current_user.is_anonymous or current_user.confirm:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirm.hmtl')
#@auth.before_app_request
#def before_request():
#   if current_user.is_authenticated and not current_user.confirm \
#        and request.endpoint and request.endpoint[:5]!='auth.' \
#        and request.endpoint !='static':
#        print(1)
#        return redirect(url_for('auth.unconfirmed'))
#@auth.route('/unconfirmed')
#def unconfirmed():
#    if current_user.is_anonymous or current_user.confirm:
#        print(2)
#        return redirect(url_for('main.index'))
#    return render_template('auth/unconfirmed.html')


@auth.route('/registe',methods=['GET','POST'])
def registe():
    form = RegisteForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,name=form.name.data)
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        token = user.generate_registe_token()
        send_email(form.email.data,'Confirm Your Account','auth/email/confirm',user=user,token=token)
        flash('A email has been sent to your email')
        return redirect(url_for('main.index'))

    return render_template('auth/registe.html',form=form)

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)

            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invali username or password')
    return render_template('auth/login.html',form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    print(current_user.confirm)
    if current_user.confirm:
        flash('You have already confirm')
        return redirect(url_for('main.index'))
    if current_user.confirmed(token):
        flash('Thanks for Confirming')
        return redirect(url_for('main.index'))
    flash('The confirm link is past due')
    return redirect(url_for('main.index'))

@auth.route('/log_out')
@login_required
def log_out():
    logout_user()
    flash('You have been out')
    return redirect(url_for('main.index'))
