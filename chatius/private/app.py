import os, datetime, pusher
from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

pusher_client = pusher.Pusher(
  app_id='568045',
  key='c11bb20f5ac00e606470',
  secret='3b73d0bf396200d229be',
  cluster='eu',
  ssl=True
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(50))
    referal = db.Column(db.String(30))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    message = db.Column(db.String(500))

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[InputRequired(), Length(min=4, message='Имя пользователя должно состоять минимум из 4 символов')])
    password = PasswordField('Пароль', validators=[InputRequired(), Length(min=8, message='Пароль должен состоять минимум из 8 символов')])

class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[InputRequired(), Length(min=4, message='Имя пользователя должно состоять минимум из 4 символов')])
    password = PasswordField('Пароль', validators=[InputRequired(), Length(min=8, message='Пароль должен состоять минимум из 8 символов')])
    email = StringField('Почта', validators=[InputRequired(), Email(message='Неверная почта'), Length(max=50)])
    referal = StringField('Имя пользователя, пригласившего вас на проект', validators=[Length(max=50)])

@app.route('/')
def index():
    refs = None
    if current_user.is_authenticated:
        refs = User.query.filter_by(referal=current_user.username).count()
    return render_template('index.html', refs=refs)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).count() != 0:
            return render_template('register.html', form=form, error="- Такое имя пользователя уже используется!!1")
        elif User.query.filter_by(email=form.email.data).count() != 0:
            return render_template('register.html', form=form, error="- Такой E-MAIL уже используется!!1")

        user = User(username = form.username.data, email = form.email.data, password=form.password.data, referal=form.referal.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)

        return redirect(url_for('chat'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user)
                return redirect(url_for('chat'))
            return render_template('login.html', form=form, error='- Неверный логин или пароль!')
        return render_template('login.html', form=form, error='- Такого пользователя не существует!')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/chat')
def chat():
    messages = Message.query.all()
    if current_user.is_authenticated:
        name = current_user.username
    else:
        name = None
    return render_template('chat.html', username=name, messages=messages)

@app.route('/message', methods=['POST'])
def message():
    username = request.form.get('username')
    message = request.form.get('message')
    new_message = Message(username=username, message=message)
    db.session.add(new_message)
    db.session.commit()
    pusher_client.trigger('chat-channel', 'new-message', {'username' : username, 'message': message})
    return jsonify({'result' : 'success'})

if __name__ == '__main__':
    app.run()
