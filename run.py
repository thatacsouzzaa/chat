from flask import Flask
from controllers import chat

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Registrar Blueprint
app.register_blueprint(chat.bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)