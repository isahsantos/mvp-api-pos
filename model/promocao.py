import datetime
from click import DateTime
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Promocao(Base):
    __tablename__ = 'promocao'
    pk_promocao = Column(Integer, primary_key=True)
    nome = Column(String(140))
    data_publicacao = Column(DateTime, default=datetime.now)
    divulgador = Column(String(100))
    url = Column(String(200))

    # Relacionamento de um para muitos com Produto
    produtos = relationship("Produto", back_populates="promocao")
