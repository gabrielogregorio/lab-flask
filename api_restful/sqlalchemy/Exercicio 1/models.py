from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///estudo.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Programador(Base):
    __tablename__ = "programadores"
    cpf = Column(String(11), primary_key=True)
    nome = Column(String(100), index=True)
    idade = Column(String(3))
    email = Column(String(100))

    def __repr__(self):
        return "<Programador: {}>".format(self.nome)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Habilidade(Base):
    __tablename__ = "habilidades"
    id = Column(Integer, primary_key=True)
    nome = Column(String(30), index=True)

    def __repr__(self):
        return "<Habilidade: {}>".format(self.nome)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

class ProgramadorHabilidade(Base):
    __tablename__ = "programador_habilidade"

    id = Column(Integer, primary_key=True)

    cpf_programador = Column(String(11), ForeignKey('programadores.cpf'))
    id_habilidade = Column(Integer, ForeignKey('habilidades.id'))

    relationship('programadores')
    relationship('habilidades')

    def __repr__(self):
        return "<ProgramadorHabilidade: {}>".format(self.cpf_programador)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

import os

if __name__ == "__main__":
    os.remove('estudo.db')
    Base.metadata.create_all(bind=engine)

        
