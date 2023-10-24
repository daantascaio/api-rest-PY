from flask import Flask, request
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='API REST O.o')
spec.register(server)


class Pessoa(BaseModel):
    id: int
    nome: str
    idade: int


@server.get('/pessoas')
def get_pessoas():
    return 'Programaticamente Falando'


@server.post('/pessoas')
@spec.validate(body=Request(Pessoa), resp=Response(HTTP_200=Pessoa))
def post_pessoas():
    """Insere pessoas no banco de dados"""
    body = request.context.body.dict()
    return body


server.run()
