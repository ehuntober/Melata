
from crypt import methods
from flask import Blueprint , render_template , url_for , redirect , request
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import current_user , login_user , login_required ,logout_user
from models import User
from app import db

from app import app

import qrcode

import secrets

auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup():
    return render_template('Signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name=request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email = email).first()

    if user:
        return redirect(url_for('auth.signup'))
    new_user = User(email=email,name=name,password = generate_password_hash(password,method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/login',methods=['GET'])
def login():
    return render_template('login.html')

@auth.route('/login',methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or  not check_password_hash(user.password, password):
        return redirect(url_for('auth.login'))
    
    login_user(user, remember = remember)

    return redirect(url_for('main.dashboard'))

import os

dir_path=os.path.dirname(os.path.realpath(__file__))
app.config.update(
    UPLOAD_PATH=os.path.join(dir_path,"static")
)


@auth.route('/generate', methods=['POST','GET'])
def index_generated():
    data = request.form.get('url')
    image_name = f"{secrets.token_hex(10)}.png"
    qrcode_location = f"{app.config['UPLOAD_PATH']}/{image_name}"
    my_qrcode = qrcode.make(str(data))
    my_qrcode.save(qrcode_location)

    return render_template('generated_qrcode.html',image = image_name)



@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
    


