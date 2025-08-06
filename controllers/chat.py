from controllers.sql import Banco  # Importa a classe Banco do módulo controllers.sql para interagir com o banco de dados
from flask import session  # Importa o objeto session do Flask para gerenciar sessões de usuários
from datetime import datetime

class Chat:  # Define a classe Chat para gerenciar mensagens no chat
    def __init__(self, mensagem):   # Método construtor da classe, inicializa a mensagem e uma instância do banco de dados
        self.mensagem = mensagem  # Armazena a mensagem recebida
        self.banco = Banco()  # Cria uma instância da classe Banco para interagir com o banco de dados
        
    def enviar_mensagem(self):  # Método para enviar uma mensagem ao banco de dados
        nome_usuario = session.get("usuario_logado")    # Obtém o usuário logado da sessão do Flask
        try:
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            dados = {
                'mensagem': f"{self.mensagem}",
                'nome_usuario': f"{nome_usuario}",
                'data_hora': f"{data_hora}" 
            } # Cria um dicionário com a mensagem formatada, incluindo o nome do usuário

            self.banco.inserir('tb_chat', dados)  # Insere a mensagem na tabela 'tb_chat' do banco de dados
            print("Chat.py | Enviar Mensagem | Enviado com sucesso")  # Exibe um log informando que a mensagem foi enviada com sucesso
        except Exception as e:  # Captura possíveis erros na execução do bloco try
            print(f"Chat.py | Enviar Mensagem | Erro ao enviar: {e}")   # Exibe um log informando que ocorreu um erro ao enviar a mensagem

    def consultar_mensagem(self):  
        try:
            dados = self.banco.consultar('tb_chat')  # Consulta todas as mensagens armazenadas
            print("Chat.py | Consultar Mensagem | Dados retornados do banco:")

            for msg in dados:  # Debug: imprime cada mensagem recuperada
                print(msg)

            return dados  # Retorna os dados obtidos da consulta
        except Exception as e:
            print(f"Chat.py | Consultar Mensagem | Erro ao consultar: {e}")
        return []  # Retorna uma lista vazia em caso de erro