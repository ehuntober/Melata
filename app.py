
import os
from dotenv import load_dotenv

load_dotenv()



from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager






app = Flask(__name__)
app.config['SECRET_KEY'] =os.getenv('SECRET_KEY')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI'] =os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
db.init_app(app)

migrate = Migrate(app,db)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from database import User

@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))

# from .main import main as main_blueprint
from main import main
app.register_blueprint(main)

# from auth import auth as auth_blueprint
from auth import auth
app.register_blueprint(auth)


if __name__ == '__main__':
        app.run(debug=False)


    
