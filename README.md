# 📦 Sistema de Estoque

Um sistema web simples de controle de estoque, construído com Flask e SQLite.

Permite cadastrar e visualizar produtos, com alerta visual automático para itens abaixo do estoque mínimo. Desenvolvido como peça de portfólio para Análise e Desenvolvimento de Sistemas.

![Screenshot do sistema](docs/listagem.png)
![Screenshot do sistema](docs/formulario.png)

## Highlights

- Cadastro e listagem de produtos (CRUD parcial).
- Alerta visual para produtos com estoque baixo.
- Preço formatado em Real (R$).
- Interface responsiva (desktop e celular).
- Banco de dados local — zero configuração.

## Requirements

- Python 3.10+
- Git

O SQLite já vem embutido no Python.

## Estrutura do projeto


sistema-estoque/
├── app.py
├── estoque.db
├── templates/
│   ├── index.html
│   └── form_produto.html
└── static/
    └── css/
        └── style.css
        

## Rotas
Rota	O que faz
/	Lista os produtos
/produtos/novo	Formulário de cadastro
Sobre o alerta de estoque

O sistema considera que um produto está com estoque baixo quando:
text

quantidade <= estoque_minimo

Essa comparação é feita direto no template (Jinja2), e a linha fica destacada em vermelho automaticamente.

## O que pretendo adicionar

    □ Editar e excluir produtos
    □ Busca por nome
    □ Filtro por categoria
    □ Histórico de entradas e saídas