import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATABASE = 'estoque.db'


# ---------- BANCO DE DADOS ----------

def get_db():
    """Abre a conexão com o banco SQLite."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Cria a tabela 'produtos' se ela ainda não existir."""
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            quantidade INTEGER NOT NULL DEFAULT 0,
            preco REAL NOT NULL DEFAULT 0,
            categoria TEXT,
            estoque_minimo INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


# ---------- ROTAS ----------

@app.route('/')
def index():
    
    """Lista todos os produtos cadastrados."""
    conn = get_db()
    produtos = conn.execute('SELECT * FROM produtos ORDER BY nome').fetchall()
    conn.close()
    return render_template('index.html', produtos=produtos)


@app.route('/produtos/novo', methods=['GET', 'POST'])
def novo_produto():

    """Exibe o formulário (GET) e salva o produto (POST)."""
    if request.method == 'POST':

        try:
            nome = request.form['nome']
            descricao = request.form['descricao']
            categoria = request.form['categoria']
            quantidade = int(request.form['quantidade'])
            preco = float(request.form['preco'].replace(',', '.'))
            estoque_minimo = int(request.form['estoque_minimo'])

        except (ValueError, KeyError) as e:
            return f"Erro ao processar os dados do produto, insira apenas valores numéricos: {e}", 400

        conn = get_db()
        conn.execute('''
            INSERT INTO produtos (nome, descricao, quantidade, preco, categoria, estoque_minimo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, descricao, quantidade, preco, categoria, estoque_minimo))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('form_produto.html')

@app.route('/produtos/<int:id>/editar', methods=['GET', 'POST'])
def editar_produto(id):
    """Edita um produto existente."""
    conn = get_db()
    
    if request.method == 'POST':

        try:
            nome = request.form['nome']
            descricao = request.form['descricao']
            categoria = request.form['categoria']

            quantidade = int(request.form['quantidade'])
            preco = float(request.form['preco'].replace(',', '.'))
            estoque_minimo = int(request.form['estoque_minimo'])
#/* se tentar colocar um valor não numérico, vai gerar ValueError, dps corrijo isso */

        except (ValueError, KeyError) as e:
            return f"Erro ao processar os dados do produto, insira apenas valores numéricos: {e}", 400

        conn.execute('''
            UPDATE produtos 
            SET nome=?, descricao=?, quantidade=?, preco=?, categoria=?, estoque_minimo=?
            WHERE id=?
        ''', (nome, descricao, quantidade, preco, categoria, estoque_minimo, id))
        
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    # Se for GET, busca o produto no banco para preencher o formulário
    produto = conn.execute('SELECT * FROM produtos WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if produto is None:
        return "Produto não encontrado", 404
        
    return render_template('form_produto.html', produto=produto)


@app.route('/produtos/<int:id>/excluir')
def excluir_produto(id):
    """Exclui um produto."""
    conn = get_db()
    conn.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# ---------- INICIALIZAÇÃO ----------

if __name__ == '__main__':
    init_db()
    app.run(debug=True)