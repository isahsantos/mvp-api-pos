from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from .produto import ProdutoSchema


class PromocaoSchema(BaseModel):
    """Define como uma promoção deve ser representada."""
    pk_promocao: int
    nome: str = Field(..., description="Nome da promoção")
    data_publicacao: datetime = Field(..., description="Data de publicação da promoção")
    divulgador: str = Field(..., description="Divulgador da promoção")
    url: str = Field(..., description="URL da promoção")
    produtos: List[ProdutoSchema] = Field(..., description="Produtos associados à promoção")


class PromocaoBuscaSchema(BaseModel):
    """Define a estrutura para busca de promoção por nome."""
    nome: str


class PromocaoDelSchema(BaseModel):
    """Define a estrutura para busca de promoção por nome."""
    id: int

class ListagemPromocoesSchema(BaseModel):
    """Define a estrutura de uma listagem de promoções."""
    promocoes: List[PromocaoSchema]

def apresenta_promocao(promocao):
    """Retorna uma representação da promoção em formato JSON."""
    return {
        "pk_promocao": promocao.pk_promocao,
        "nome": promocao.nome,
        "data_publicacao": promocao.data_publicacao.strftime("%Y-%m-%d %H:%M:%S"),
        "divulgador": promocao.divulgador,
        "url": promocao.url,
        "produtos": [apresenta_produto(produto) for produto in promocao.produtos]
    }

def apresenta_produto(produto):
    """Retorna uma representação do produto em formato JSON."""
    return {
        "pk_produto": produto.pk_produto,
        "nome": produto.nome,
        "valor": str(produto.valor),
        "categoria": produto.categoria,
        "promocao_id": produto.promocao_id
    }


def apresenta_promocoes(promocoes):
    """Retorna uma lista de representações de promoções."""
    return [apresenta_promocao(promocao) for promocao in promocoes]

class PromocaoInsertSchema(BaseModel):
    nome: str = Field(..., description="Nome da promoção")
    divulgador: str = Field(..., description="Divulgador da promoção")
    url: str = Field(..., description="URL da promoção")
    produtos: List[ProdutoSchema] = Field(..., description="Produtos associados à promoção")