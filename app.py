
import os

from flask import Flask 

from dotenv import load_dotenv
load_dotenv()

from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
from flask_login import LoginManager

db = SQLAlchemy()

app = Flask(__name__)
app.config['SECRET_KEY']= os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] =os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
        
db.init_app(app)
        
migrate = Migrate(app,db)
login_manager = LoginManager()
        
login_manager.init_app(app)
        
from models import User
        
@login_manager.user_loader
        
def load_user(user_id):
        return User.query.get(int(user_id))
                
from main import main
app.register_blueprint(main)
        
from auth import auth
app.register_blueprint(auth)

        # return app
        

# if __name__ == '__main__':
#         app.run(debug=True)
