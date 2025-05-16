from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Tabela de Usuários
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    nivel = db.Column(db.Integer, default=1)
    itens = db.relationship('Item', backref='usuario', lazy=True)

    def __repr__(self):
        return f"<Usuario {self.nome}>"

# Tabela de Itens
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_item = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def __repr__(self):
        return f"<Item {self.nome_item}>"
