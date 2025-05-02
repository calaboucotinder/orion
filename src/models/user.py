from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(255), unique=True, nullable=False)
    telefone = db.Column(db.String(50), unique=True, nullable=False)
    codigo_acesso = db.Column(db.String(50), unique=True, nullable=False)
    respostas_quiz = db.Column(db.JSON, nullable=True)  # SQLite suporta JSON nativamente
    resumo_gerado = db.Column(db.Text, nullable=True)
    idioma = db.Column(db.String(10), nullable=False, default='pt')
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Usuario {self.nick}>'

