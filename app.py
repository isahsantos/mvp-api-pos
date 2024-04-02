from datetime import datetime
from http.client import HTTPException
from flask import Flask, jsonify, make_response, request

from schema import *
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from model import Session, Produto, Promocao
from flask_cors import CORS
import urllib.parse
from fastapi.responses import JSONResponse

from schema.error import ErrorSchema
from schema.produto import apresenta_produto
from schema.promocao import ListagemPromocoesSchema, apresenta_promocoes
from logger import logger

info = Info(  
    title="API de Produtos e Promoções",
    summary= "API de Produtos e Promoções para a aplicação web sharedPromo , listagem de todas promoções divulgadas ",
    version="1.0.0",
    contact={
        "name": "Maria Isabela dos Santos Silva (author)",
        "email": "isa2014mgspn@gmail.com",
    },
    license={"name": "Apache", "url": "https://www.apache.org/licenses/LICENSE-2.0.html"},)
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Lista dos metódos disponíveis na aplicação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base")
promocao_tag = Tag(name="Promoções", description="Adição, visualização, ou remoção de uma promoção a base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.get('/produtos', tags=[produto_tag], responses={"200": ProdutoSchema, "404": {"description": "Produtos não encontrados"}})
def get_produtos():
    """Faz a busca por todos os Produtos cadastrados na base de dados 

    Retorna uma representação da listagem de produtos.
    """
    session = Session()
    produtos = session.query(Produto).all()

    if not produtos:
        logger.info("Nenhum produto encontrado na base de dados")
        return {"produtos": []}, 404

    produtos_json = []
    for produto in produtos:
        produto_data = apresenta_produto(produto) 
        if produto.promocao:
            produto_data['url_promocao'] = produto.promocao.url 
        produtos_json.append(produto_data)

    logger.info("Produtos encontrados na base de dados")
    return jsonify(produtos_json), 200


@app.post('/produtos/busca-por-nome', tags=[produto_tag])
def get_produto_by_name(form: ProdutoBuscaSchema):
    """Faz a busca por um produto informando seu nome no corpo da requisição."""
    nome = form.nome

    if not nome:
        return jsonify({"mensagem": "Nome do produto não fornecido"}), 400

    nome = urllib.parse.unquote(nome)

    session = Session()
    
    produto = session.query(Produto).filter(Produto.nome == nome).first()

    if not produto:
        return jsonify({"mensagem": "Produto não encontrado"}), 404

    if produto.promocao_id:
        promocao = session.query(Promocao).filter(Promocao.pk_promocao == produto.promocao_id).first()
        url_promocao = promocao.url if promocao else None
    else:
        url_promocao = None
        
    return jsonify({
        "nome": produto.nome,
        "categoria": produto.categoria,
        "valor": produto.valor,
        "url_promocao": url_promocao,
        "id_produto": produto.pk_produto
    }), 200

@app.post('/cadastrar-produto', tags=[produto_tag],
          responses={"201": ProdutoSchema})
def criar_produto(form: ProdutoSchema):
    """Cadastra um novo produto no banco de dados."""
    data = form
    if not data:
        logger.error("Dados do produto não fornecidos")
        return {"mensagem": "Dados do produto não fornecidos"}, 400
    
    nome = form.nome
    valor = form.valor
    categoria = form.categoria
    promocao_id = form.promocao_id

    if not nome or not valor or not categoria or promocao_id is None:
        logger.error("Nome, valor, categoria e ID da promoção do produto são obrigatórios")
        return {"mensagem": "Nome, valor, categoria e ID da promoção do produto são obrigatórios"}, 400

    novo_produto = Produto(nome=nome, valor=valor, categoria=categoria, promocao_id=promocao_id)  
    session = Session()
    session.add(novo_produto)
    session.commit()

    logger.info("Produto cadastrado com sucesso")
    return jsonify({
        "id": novo_produto.pk_produto,
        "nome": novo_produto.nome,
        "valor": novo_produto.valor,
        "categoria": novo_produto.categoria,
        "promocao_id": novo_produto.promocao_id
    }), 201


@app.delete('/remover-produto', tags=[produto_tag],
            responses={"200": {"description": "Produto removido com sucesso"}})
def del_produto(form: ProdutoDelSchema):
    """Deleta um Produto a partir do ID informado no corpo da requisição

    Retorna uma mensagem de confirmação da remoção.
    """
    data = form.produto_id 
    if not data:
        logger.error("ID do produto não fornecido")
        return {"message": "ID do produto não fornecido"}, 400
    
    produto_id = data

    session = Session()
    produto = session.query(Produto).filter(Produto.pk_produto == produto_id).first()

    if produto:
        session.delete(produto)
        session.commit()

        logger.info(f"Produto {produto_id} removido com sucesso")
        return {"message": "Produto removido", "id": produto_id}, 200
    else:
        logger.error("Produto não encontrado na base")
        return {"message": "Produto não encontrado na base"}, 404


@app.get('/promocoes', tags=[promocao_tag],
         responses={"200": ListagemPromocoesSchema, "404": {"description": "Promoções não encontradas"}})
def get_promocoes():
    """Busca todas as promoções cadastradas no banco de dados.

    Retorna uma representação da listagem de promoções.
    """
    session = Session()

    promocoes = session.query(Promocao).all()

    if not promocoes:
        logger.info("Nenhuma promoção encontrada na base de dados")
        return jsonify({"promocoes": []}), 404

    promocoes_json = [apresenta_promocao(promocao) for promocao in promocoes]

    session.close()

    logger.info("Promoções encontradas na base de dados")
    return jsonify(promocoes_json), 200


@app.post('/promocoes/busca-por-nome', tags=[promocao_tag],
          responses={"200": {"description": "Promoção encontrada com sucesso"}, "404": {"description": "Promoção não encontrada"}})
def get_promocao_by_name(form: PromocaoBuscaSchema):
    """Busca uma promoção pelo nome fornecido no corpo da requisição.

    Retorna uma representação da promoção encontrada.
    """
    if not form.nome:
        logger.error("Nome da promoção não fornecido")
        return jsonify({"mensagem": "Nome da promoção não fornecido"}), 400

    nome_promocao = form.nome

    session = Session()

    promocao = session.query(Promocao).filter(Promocao.nome == nome_promocao).first()

    if not promocao:
        logger.info("Promoção não encontrada")
        return jsonify({"mensagem": "Promoção não encontrada"}), 404

    promocao_json = apresenta_promocao(promocao)

    session.close()

    logger.info("Promoção encontrada")
    return jsonify(promocao_json), 200


@app.post('/cadastrar-promocao', tags=[promocao_tag], responses={"201": {"description": "Promoção cadastrada com sucesso"}, "400": {"description": "Campos obrigatórios não fornecidos"}})
def cadastrar_promocao(form: PromocaoInsertSchema):
    # Verifica se todos os campos obrigatórios foram fornecidos
    campos_necessarios = form.nome, form.divulgador, form.url
    for campo in campos_necessarios:
        if campo is None:
            return jsonify({"mensagem": f"O campo '{campo}' é obrigatório"}), 400

    # Cria uma nova promoção com os dados fornecidos
    nova_promocao = Promocao(
        nome=form.nome,
        divulgador=form.divulgador,
        url=form.url
    )

    # Adiciona a nova promoção ao banco de dados
    session = Session()
    session.add(nova_promocao)
    session.commit()

    # Adiciona os produtos associados à promoção
    for produto in form.produtos:
        novo_produto = Produto(nome=produto.nome, promocao=nova_promocao)
        session.add(novo_produto)
    session.commit()

    session.close()

    return jsonify({"mensagem": "Promoção cadastrada com sucesso"}), 201

@app.delete('/remover-promocao', tags=[promocao_tag], responses={"200": {"description": "Promoção excluída com sucesso"}, "404": {"description": "Promoção não encontrada"}})
def delete_promocao(form: PromocaoDelSchema):
    promocao_id = form.id

    if not promocao_id:
        return jsonify({"mensagem": "ID da promoção não fornecido"}), 400

    session = Session()

    # Busca a promoção no banco de dados pelo ID fornecido
    promocao = session.query(Promocao).filter_by(pk_promocao=promocao_id).first()

    if not promocao:
        return jsonify({"mensagem": "Promoção não encontrada"}), 404

    # Remove a promoção do banco de dados
    session.delete(promocao)
    session.commit()

    return jsonify({"mensagem": "Promoção excluída com sucesso"}), 200

if __name__ == '__main__':
    app.run(debug=True)