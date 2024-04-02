from sqlalchemy.orm import relationship
from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime
from model.base import Base

from sqlalchemy.orm import relationship

class Produto(Base):
    __tablename__ = 'produto'
    pk_produto = Column(Integer, primary_key=True)
    nome = Column(String(140))
    valor = Column(Float)
    categoria = Column(String(100))
    promocao_id = Column(Integer, ForeignKey('promocao.pk_promocao'))  # Chave estrangeira para o ID da promoção

    promocao = relationship("Promocao", back_populates="produtos")
