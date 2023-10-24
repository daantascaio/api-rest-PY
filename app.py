from itertools import count
from typing import Optional
from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel, Field
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='API REST O.o')
spec.register(server)
database = TinyDB(storage=MemoryStorage)
c = count()


class Pessoa(BaseModel):
    id: Optional[int] = Field(default_factory=lambda: next(c))
    nome: str
    idade: int


class Pessoas(BaseModel):
    pessoas: list[Pessoa]
    count: int


@server.get('/pessoas')
@spec.validate(resp=Response(HTTP_200=Pessoas))
def get_pessoas():
    """Retorna todas as pessoas da base de dados"""

    return jsonify(Pessoas(pessoas=database.all(), count=len(database.all())).dict())


@server.get('/pessoas/<int:id>')
@spec.validate(resp=Response(HTTP_200=Pessoa))
def get_pessoa(id):
    """Retorna uma pessoa da base de dados"""
    try:
        pessoa = database.search(Query().id == id)[0]
    except IndexError:
        return {'message': 'Pessoa not found!'}, 404
    return jsonify(pessoa)


@server.post('/pessoas')
@spec.validate(body=Request(Pessoa), resp=Response(HTTP_200=Pessoa))
def post_pessoas():
    """Insere pessoas no banco de dados"""
    body = request.context.body.dict()
    database.insert(body)
    return body


@server.put('/pessoas/<int:id>')
@spec.validate(
    body=Request(Pessoa), resp=Response(HTTP_200=Pessoa)
)
def put_pessoa(id):
    """Altera pessoa"""
    Pessoa = Query()
    body = request.context.body.dict()
    database.update(body, Pessoa.id == id)
    return jsonify(body)


@server.delete('/pessoas/<int:id>')
@spec.validate(resp=Response('HTTP_204'))
def delete_pessoa(id):
    """Deleta pessoa"""
    Pessoa = Query()
    database.remove(Pessoa.id == id)
    return jsonify({})


server.run(debug=True)
