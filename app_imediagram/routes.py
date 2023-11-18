from flask import Flask, render_template, url_for, redirect, request
from app_imediagram import app, bcrypt, database
from app_imediagram.forms import FormLogin, FormCriarConta, FormFoto
from flask_login import login_required, login_user, logout_user, current_user
from app_imediagram.models import Usuario, Foto
from werkzeug.utils import secure_filename
import os

@app.route('/', methods = ["GET", "POST"])
def homepage():
    formLogin = FormLogin()
    if formLogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email = request.form['email']).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, request.form['senha']):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario = usuario.id))
    return render_template('homepage.html', form = formLogin)

@app.route('/criar-conta', methods = ["GET", "POST"])
def criarconta():
    formCriarConta = FormCriarConta()
    if formCriarConta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formCriarConta.senha.data).decode('utf-8')        
        usuario = Usuario(username = formCriarConta.data['username'], email = formCriarConta.data['email'], senha = senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember = True)
        return redirect(url_for("perfil", id_usuario = usuario.id))
    return render_template('criarconta.html', form = formCriarConta)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route('/feed')
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template('feed.html', fotos = fotos)

@app.route('/perfil/<int:id_usuario>', methods = ["GET", "POST"])
@login_required
def perfil(id_usuario):
    usuario = Usuario.query.get(int(id_usuario))
    fotos = Foto.query.filter_by(id_usuario=id_usuario).order_by(Foto.data_criacao.desc()).all()
    
    if  usuario.id == int(current_user.id):
        formFoto = FormFoto()

        if formFoto.validate_on_submit():
            arquivo = request.files['foto']
            nome_do_arquivo = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], nome_do_arquivo)
            arquivo.save(caminho)
            foto = Foto(imagem = nome_do_arquivo, id_usuario = current_user.id)
            database.session.add(foto)
            database.session.commit()
            fotos.insert(0, foto)  # Adiciona a nova foto no início da lista
        
        return render_template('perfil.html', usuario = usuario, form = formFoto, fotos = fotos)
    else:
        return render_template('perfil.html', usuario = usuario, form = None, fotos = fotos)

'''    
@app.route('/criar-usuario-imediagram')
def criar_usuario_teste():
    # Verifica se já existe um usuário de teste
    usuario_imediagram = Usuario.query.filter_by(username='Imediagram').first()
    if usuario_imediagram:
        return "Usuário de teste já existe."

    # Cria um novo usuário de teste
    senha_imediagram = bcrypt.generate_password_hash('Imed@Adm001').decode('utf-8')
    novo_usuario_imediagram = Usuario(username='Imediagram', senha=senha_imediagram, email='imediagram@imediagram.com')
    database.session.add(novo_usuario_imediagram)
    database.session.commit()

    return "Usuário de teste criado com sucesso."

import shutil
from flask import send_from_directory, current_app

@app.route('/adicionar_foto/<int:id_usuario>')
@login_required
def adicionar_foto(id_usuario):
    nome_imagem = 'imagem.jpg'
    caminho_imagem = os.path.join(current_app.root_path, 'static', 'fotos_posts', nome_imagem)
    caminho_destino = app.config['UPLOAD_FOLDER']

    try:
        # Move o arquivo para o diretório de destino
        shutil.move(caminho_imagem, os.path.join(caminho_destino, nome_imagem))

        foto = Foto(imagem=nome_imagem, id_usuario=id_usuario)
        database.session.add(foto)
        database.session.commit()

        # Envia o arquivo como resposta
        return send_from_directory(caminho_destino, nome_imagem, as_attachment=True)
    except Exception as e:
        return f"Foto não adicionada: {e}"
'''