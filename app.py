from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel
from tinydb import TinyDB, Query

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='API REST O.o')
spec.register(server)
database = TinyDB('database.json')


class Pessoa(BaseModel):
    id: int
    nome: str
    idade: int


@server.get('/pessoas')
def get_pessoas():
    """Retorna todas as pessoas da base de dados"""
    return jsonify(database.all())


@server.post('/pessoas')
@spec.validate(body=Request(Pessoa), resp=Response(HTTP_200=Pessoa))
def post_pessoas():
    """Insere pessoas no banco de dados"""
    body = request.context.body.dict()
    database.insert(body)
    return body


server.run(debug=True)
