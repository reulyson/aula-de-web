import sqlite3
from flask import Flask, render_template, request, g, redirect, url_for, \
    abort, session, flash

# Configurações

DATABASE = './tmp/flaskr.db'
USERNAME = 'admin'
PASSWORD = '123456'

# Criando o App
app = Flask(__name__)

def conectar_bd():
    return sqlite3.connect(DATABASE)

@app.before_request
def pre_requisicao():
    g.bd = conectar_bd()

@app.teardown_request
def pos_requisicao(exception):
    g.bd.close()

@app.route('/')
def exibir_entradas():
    sql = "SELECT titulo, texto FROM entradas ORDER BY id DESC"
    cursor = g.bd.execute(sql)
    entradas = [dict(titulo=titulo, texto=texto) for titulo, texto in cursor.fetchall()]
    return render_template('exibir_entradas.html')

@app.route('/inserir', methods=['POST'])
def inserir_entrada():
    if not session.get('logado'):
        abort(401)
    sql = "INSERT INTO entradas (titulo, texto) VALUES (?, ?)"
    g.bd.execute(sql, [request.form['titulo'], request.form['texto']])
    g.bd.commit()
    flash('Nova entrada salva com sucesso!')
    return redirect(url_for('exibir_entradas'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        if request.form['username'] != USERNAME:
            erro = "Usuário Inválido"
        elif request.form['password'] != PASSWORD:
            erro = 'Senha inválida'
        else:
            session['logado'] = True
            flash('Logado com Sucesso. Bem-vindo!')
            return redirect(url_for('exibir_entradas'))
    return render_template('login.html', erro=erro)

@app.route('/logout')
def logout():
    session.pop('logado', None)
    flash('O logout foi feito com sucesso')
    return redirect(url_for('exibir_entradas'))