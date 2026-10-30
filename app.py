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
        nome = request.form['nome']
        descricao = request.form['descricao']
        categoria = request.form['categoria']
        quantidade = int(request.form['quantidade'])
        preco = float(request.form['preco'].replace(',', '.'))
        estoque_minimo = int(request.form['estoque_minimo'])

        conn = get_db()
        conn.execute('''
            INSERT INTO produtos (nome, descricao, quantidade, preco, categoria, estoque_minimo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, descricao, quantidade, preco, categoria, estoque_minimo))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('form_produto.html')


# ---------- INICIALIZAÇÃO ----------

if __name__ == '__main__':
    init_db()
    app.run(debug=True)