from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO
from controllers.sql import Banco
from controllers.chat import Chat
import sqlite3

app = Flask(__name__)
app.secret_key = "chave_super_secreta"  # Necessário para gerenciar sessões
app.config['banco_de_dados'] = []
socketio = SocketIO(app)
app.config['SECRET_KEY'] = '1234'


def get_db_connection():
    return sqlite3.connect('models/chat.db')


# Página inicial
@app.route('/')
def index():
    return render_template('index.html')


# Cadastro de usuários
@app.route('/cadastro', methods=['POST', 'GET'])
def cadastrousuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        nome_usuario = request.form.get('nome_usuario')
        telefone = request.form.get('telefone')

        if not nome or not nome_usuario or not senha:
            print("Erro: Campos obrigatórios faltando")
            return render_template('cadastro.html', erro="Preencha todos os campos obrigatórios.")

        try:
            with sqlite3.connect('models/chat.db') as conexao:
                cursor = conexao.cursor()
                sql = '''INSERT INTO tb_usuarios (nome, senha, nome_usuario, telefone) VALUES (?, ?, ?, ?)'''
                cursor.execute(sql, (nome, senha, nome_usuario, telefone))
                conexao.commit()
                return redirect('/login')

        except sqlite3.Error as e:
            print(f"Erro no banco de dados: {e}")
            return render_template('cadastro.html', erro=f"Erro ao acessar banco de dados: {e}")

    return render_template('cadastro.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome_usuario = request.form.get('nome_usuario')
        senha = request.form.get('senha')

        with sqlite3.connect('models/chat.db') as conexao:
            cursor = conexao.cursor()
            sql = '''SELECT * FROM tb_usuarios WHERE nome_usuario = ? AND senha = ?'''
            cursor.execute(sql, (nome_usuario, senha))
            user = cursor.fetchone()

        if user:
            session['usuario_logado'] = user[3]  # user[3] é o nome_usuario
            print(f"Login bem-sucedido para: {user}")
            return redirect('/chat', code=302)
        else:
            return render_template('login.html', erro="Usuário ou senha incorretos.")

    return render_template('login.html')


# Página do chat
@app.route('/chat', methods=['POST', 'GET'])
def chat():
    if 'usuario_logado' not in session:
        print("Usuário não autenticado. Redirecionando para login.")
        return redirect('/login', code=302)

    usuario = session['usuario_logado']
    print(f"Usuário na página de chat: {usuario}")
    chat_obj = Chat(usuario)

    if request.method == 'POST':
        mensagem = request.form.get('mensagem')
        if mensagem:
            chat_obj.mensagem = mensagem
            chat_obj.enviar_mensagem()
            socketio.emit('atualizar')

    mensagens = chat_obj.consultar_mensagem()
    return render_template('chat.html', mensagens=mensagens, usuario=usuario)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=80, debug=True)
