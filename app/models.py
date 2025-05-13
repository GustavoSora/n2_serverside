from app import mysql

# criando primeira classe do BD
class User(mysql.Model):
    id = mysql.Column(mysql.Integer, primary_key=True)
    name = mysql.Column(mysql.String(120), index=True, unique=True)
    email = mysql.Column(mysql.String(100), index=True, unique=True)

    # criar funcao para transformar obj em dicionario (tem lugar que pede)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }