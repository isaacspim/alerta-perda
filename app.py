import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Produto, RegistroPerda

app = Flask(__name__)
app.config['SECRET_KEY'] = 'integrador'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alerta_perda.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Cria as tabelas no SQLite na primeira execução
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    produtos = Produto.query.order_by(Produto.data_validade.asc()).all()
    return render_template('index.html', produtos=produtos)

@app.route('/produto/novo', methods=['GET', 'POST'])
def novo_produto():
    if request.method == 'POST':
        nome = request.form.get('nome')
        categoria = request.form.get('categoria')
        codigo_barras = request.form.get('codigo_barras')
        validade_str = request.form.get('data_validade')
        quantidade = float(request.form.get('quantidade_estoque', 0))
        unidade = request.form.get('unidade_medida', 'kg')

        data_validade = datetime.strptime(validade_str, '%Y-%m-%d').date()

        produto = Produto(
            nome=nome,
            categoria=categoria,
            codigo_barras=codigo_barras,
            data_validade=data_validade,
            quantidade_estoque=quantidade,
            unidade_medida=unidade
        )
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('novo_produto.html')

@app.route('/produto/<int:produto_id>/baixa', methods=['GET', 'POST'])
def registrar_baixa(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    
    if request.method == 'POST':
        quantidade = float(request.form.get('quantidade_perdida', 0))
        motivo = request.form.get('motivo')
        observacao = request.form.get('observacao', '')

        # Cria o registro de perda no banco
        registro = RegistroPerda(
            produto_id=produto.id,
            quantidade_perdida=quantidade,
            motivo=motivo,
            observacao=observacao
        )
        
        # Abate a quantidade do estoque atual
        produto.quantidade_estoque = max(0.0, produto.quantidade_estoque - quantidade)
        
        db.session.add(registro)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('registrar_baixa.html', produto=produto)

@app.route('/api/produtos/alertas')
def api_alertas():
    produtos = Produto.query.filter(Produto.data_validade <= date.today()).all()
    return {
        "total": len(produtos),
        "itens": [{"nome": p.nome, "dias": p.dias_para_vencer, "categoria": p.categoria} for p in produtos]
    }

if __name__ == '__main__':
    app.run(debug=True)