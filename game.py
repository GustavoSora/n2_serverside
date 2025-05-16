from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import Usuario, Item
from app import app, db


# Página do perfil do usuário
@app.route('/perfil')
@login_required
def perfil():
    usuario = current_user
    itens = Item.query.filter_by(usuario_id=usuario.id).all()
    return render_template('perfil.html', usuario=usuario, itens=itens)

# Rota para adicionar item
@app.route('/adicionar_item', methods=['POST'])
@login_required
def adicionar_item():
    item_nome = request.form['item_nome']
    item = Item(nome_item=item_nome, usuario_id=current_user.id)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('perfil'))
