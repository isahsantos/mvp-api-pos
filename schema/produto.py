from pydantic import BaseModel, Field
from typing import Optional, List
from model.produto import Produto


class ProdutoSchema(BaseModel):
    """ Define como um novo produto deve ser registrado
    """
    id: str  = Field(..., description="Id do produto")
    nome: str  = Field(..., description="Nome do produto")
    categoria: str = Field(..., description="Categoria, exemplo: eletrônico")
    valor: float =  Field(..., description="Preço $valor.00")
    promocao_id: int  =  Field(..., description="Id da promocao em que o produto está associado")


def apresenta_produto(produto):
    return {
        "id": produto.pk_produto,
        "nome": produto.nome,
        "valor": produto.valor,
        "categoria": produto.categoria,
        "promocao_id": produto.promocao_id
    }


class ProdutoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca, que será
        feita apenas com base no nome do produto.
    """
    nome: str = "Produto 1"


class ListagemProdutosSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    produtos: List[ProdutoSchema]


def apresenta_produtos(produtos: List[Produto]):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoSchema.
    """
    produtos_list = []
    for produto in produtos:
        produtos_list.append({
            "id": produto.pk_produto,
            "nome": produto.nome,
            "valor": produto.valor,
            "categoria": produto.categoria,
            "promocao_id": produto.promocao_id
        })
    return produtos_list


class ProdutoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    produto_id: str
