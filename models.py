from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    cargo = db.Column(db.String(50), nullable=False, default='Fiscal de Loja')
    
    perdas_registradas = db.relationship('RegistroPerda', backref='responsavel', lazy=True)
    inspecoes = db.relationship('InspecaoSetor', backref='fiscal', lazy=True)

    def __repr__(self):
        return f"{self.nome} ({self.cargo})"


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
    lotes = db.relationship(
        'Lote', backref='produto', lazy=True, cascade='all, delete-orphan'
    )

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


class Lote(db.Model):
    __tablename__ = 'lotes'
    __table_args__ = (
        db.UniqueConstraint('produto_id', 'codigo_lote', name='uq_lote_por_produto'),
    )

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    codigo_lote = db.Column(db.String(50), nullable=False)
    data_entrada = db.Column(db.Date, nullable=False, default=date.today)
    data_validade = db.Column(db.Date, nullable=False)
    quantidade_inicial = db.Column(db.Float, nullable=False)
    quantidade_atual = db.Column(db.Float, nullable=False)
    local_armazenamento = db.Column(db.String(100), nullable=True)

    @property
    def dias_para_vencer(self):
        return (self.data_validade - date.today()).days

    @property
    def status_alerta(self):
        dias = self.dias_para_vencer
        if self.quantidade_atual <= 0:
            return {'tipo': 'secondary', 'texto': 'Sem saldo'}
        if dias < 0:
            return {'tipo': 'danger', 'texto': 'Vencido (Descarte Imediato)'}
        if dias <= 2:
            return {'tipo': 'warning', 'texto': 'Ação Comercial / Promoção Urgente'}
        if dias <= 5:
            return {'tipo': 'info', 'texto': 'Atenção / Giro Rápido'}
        return {'tipo': 'success', 'texto': 'Regular'}


class InspecaoSetor(db.Model):
    __tablename__ = 'inspecoes_setor'
    
    id = db.Column(db.Integer, primary_key=True)
    fiscal_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    setor = db.Column(db.String(50), nullable=False)  # Ex: Ilha de Congelados, Balcão Carnes, Gôndola FLV
    temperatura_aferida = db.Column(db.Float, nullable=True)  # Em °C
    status_conformidade = db.Column(db.String(30), nullable=False)  # Conforme, Alerta, Crítico
    observacao = db.Column(db.Text, nullable=True)
    data_inspecao = db.Column(db.DateTime, default=datetime.now)


class RegistroPerda(db.Model):
    __tablename__ = 'registros_perda'
    
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    quantidade_perdida = db.Column(db.Float, nullable=False)
    motivo = db.Column(db.String(100), nullable=False)
    data_registro = db.Column(db.DateTime, default=datetime.now)
    observacao = db.Column(db.Text, nullable=True)
