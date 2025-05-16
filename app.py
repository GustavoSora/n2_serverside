from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config

# Inicialização da aplicação Flask
app = Flask(__name__)

# Configuração do banco de dados MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@{config.MYSQL_HOST}/{config.MYSQL_DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = config.SECRET_KEY

# Inicialização do banco de dados
db = SQLAlchemy(app)

# Inicialização do Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"  # Página de login

# Importação dos modelos
from models import Usuario, Item
from auth import *
from game import *

if __name__ == '__main__':
    # Inicia o servidor Flask
    app.run(debug=True)
