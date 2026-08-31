from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    codigo_barras = db.Column(db.String(50), unique=True, nullable=False)
    data_validade = db.Column(db.Date, nullable=False)
    quantidade_estoque = db.Column(db.Float, nullable=False, default=0.0)
    unidade_medida = db.Column(db.String(10), nullable=False, default='kg')
    
    perdas = db.relationship('RegistroPerda', backref='produto', lazy=True)

    @property
    def dias_para_vencer(self):
        if self.data_validade:
            return (self.data_validade - date.today()).days
        return 999

    @property
    def status_alerta(self):
        dias = self.dias_para_vencer
        if dias < 0:
            return {'tipo': 'danger', 'texto': 'Vencido (Descarte Imediato)'}
        elif dias <= 2:
            return {'tipo': 'warning', 'texto': 'Ação Comercial / Promoção Urgente'}
        elif dias <= 5:
            return {'tipo': 'info', 'texto': 'Atenção / Giro Rápido'}
        return {'tipo': 'success', 'texto': 'Regular'}


class RegistroPerda(db.Model):
    __tablename__ = 'registros_perda'
    
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade_perdida = db.Column(db.Float, nullable=False)
    motivo = db.Column(db.String(100), nullable=False)
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)
    observacao = db.Column(db.Text, nullable=True)