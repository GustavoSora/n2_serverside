from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import config

app = Flask(__name__)

# Configurações do MySQL
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)

# Página principal com lista de usuários
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios")
    dados = cur.fetchall()
    cur.close()
    return render_template('index.html', usuarios=dados)

# Rota para adicionar novo usuário
@app.route('/add', methods=['POST'])
def add_usuario():
    nome = request.form['nome']
    email = request.form['email']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuarios (nome, email) VALUES (%s, %s)", (nome, email))
    mysql.connection.commit()
    cur.close()

    return redirect('/')

# Rota para editar usuário
@app.route('/edit', methods=['POST'])
def edit_usuario():
    user_id = request.form['id']
    novo_nome = request.form['nome']
    novo_email = request.form['email']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE usuarios SET nome = %s, email = %s WHERE id = %s", (novo_nome, novo_email, user_id))
    mysql.connection.commit()
    cur.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
