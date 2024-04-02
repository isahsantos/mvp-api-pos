from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Criando a conexão com o banco de dados
engine = create_engine('sqlite:///promocoes.db', echo=True)  # Troque para o tipo de banco que desejar

# Criando uma sessão
Session = sessionmaker(bind=engine)
session = Session()

# Criando a base declarativa
Base = declarative_base()


# Definindo a tabela Produto
class Produto(Base):
    __tablename__ = 'produto'
    pk_produto = Column(Integer, primary_key=True)
    nome = Column(String(140))
    valor = Column(Float)
    categoria = Column(String(100))
    promocao_id = Column(Integer, ForeignKey('promocao.pk_promocao'))  # Chave estrangeira para o ID da promoção

    # Definindo o relacionamento com a promoção
    promocao = relationship("Promocao", back_populates="produtos")


# Definindo a tabela Promocao
class Promocao(Base):
    __tablename__ = 'promocao'
    pk_promocao = Column(Integer, primary_key=True)
    nome = Column(String(140))
    data_publicacao = Column(DateTime, default=datetime.now)
    divulgador = Column(String(100))
    url = Column(String(200))

    # Relacionamento de um para muitos com Produto
    produtos = relationship("Produto", back_populates="promocao")

# Criando as tabelas no banco de dados
Base.metadata.create_all(engine)
