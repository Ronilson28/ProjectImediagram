from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os;

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///comunidade.db'
app.config['SECRET_KEY'] = "bdca7262d580b2b6f1634c0a74658a98"
app.config['UPLOAD_FOLDER'] = os.path.join("app_imediagram", "static", "images", "fotos_posts")

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#gerenciar o login de usuário
login_manager = LoginManager(app)
# usuário não logado é direcionado para a rota principal, no caso "homepage"
login_manager.login_view = "homepage"

from app_imediagram import routes