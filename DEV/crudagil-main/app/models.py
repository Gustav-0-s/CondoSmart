from flask_login import UserMixin
from app import db
from datetime import datetime
from app import db



class Projeto(db.Model):
    projeto_id = db.Column(db.Integer, primary_key=True)
    nome_projeto = db.Column(db.String(255))
    descricao = db.Column(db.String(500))
    data_inicio = db.Column(db.Date)
    data_termino = db.Column(db.Date)
    prioridade = db.Column(db.String(10), nullable=False) 

class Sprint(db.Model):
    sprint_id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.projeto_id'))
    nome_sprint = db.Column(db.String(255))
    descricao = db.Column(db.String(500))
    data_inicio = db.Column(db.Date)
    data_termino = db.Column(db.Date)
    status = db.Column(db.String(10))
    responsavel = db.Column(db.String(255))

class Usuario(db.Model, UserMixin):
    usuario_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50))
    nome = db.Column(db.String(255))
    funcao = db.Column(db.String(100))
    senha = db.Column(db.String(8))


    def is_active(self):
        # Adicione lógica aqui para determinar se o usuário está ativo
        # Por exemplo, você pode verificar se o usuário foi suspenso ou banido
        return True  # Substitua isso pela lógica real

    def get_id(self):
        return str(self.usuario_id)

class Agendamento(db.Model):
    agendamento_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'), nullable=False)
    nome_pet = db.Column(db.String(100))
    tipo_servico = db.Column(db.String(100))  # Ex: Passeio, Cuidados Gerais, etc.
    data_hora = db.Column(db.DateTime, nullable=False)
    observacoes = db.Column(db.String(500))

    usuario = db.relationship('Usuario', backref='agendamentos', lazy=True)

    def __repr__(self):
        return f'<Agendamento {self.agendamento_id} - {self.nome_pet} - {self.tipo_servico}>'
    
    