# app/__init__.py

from flask import Flask
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Inicialização da aplicação Flask
app = Flask(__name__)
app.secret_key = 'cesusc'

# Configurações do banco de dados MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/crudagil'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização da extensão SQLAlchemy
db = SQLAlchemy(app)

# Importação das rotas e modelos
from app import routes, models

# Configuração do Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Configuração do user_loader
@login_manager.user_loader
def load_user(user_id):
    return models.Usuario.query.get(int(user_id))