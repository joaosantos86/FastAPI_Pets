import logging

from fastapi import FastAPI, HTTPException, Path, Query, Request
from fastapi.responses import JSONResponse
from mysql.connector import Error as MySQLError

from database import executar_sql

app = FastAPI(title="API de pets e tutores — Projeto Integrador II")


@app.exception_handler(MySQLError)
def erro_de_banco(request: Request, exc: MySQLError):
    logging.getLogger("uvicorn.error").error("Erro no MySQL: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Não foi possível acessar o banco de dados."},
    )


def resposta_didatica(dados, sql, parametros=()):
    return {"dados": dados, "didatica": {"sql": sql, "parametros": list(parametros)}}


@app.get("/listartutores", include_in_schema=False)
@app.get("/tutores", summary="Listar tutores")
def listartutores():
    sql = "SELECT id, nome, telefone FROM tutores ORDER BY id"
    tutores = executar_sql(sql)
    return resposta_didatica(tutores, sql)


@app.get("/consultartutor/{id}", include_in_schema=False)
@app.get("/tutores/{id}", summary="Consultar tutor por ID")
def consultartutor(id: int = Path(gt=0)):
    sql = "SELECT id, nome, telefone FROM tutores WHERE id = %s"
    parametros = (id,)
    tutores = executar_sql(sql, parametros)
    if not tutores:
        raise HTTPException(status_code=404, detail="Tutor não encontrado")
    return resposta_didatica(tutores[0], sql, parametros)


@app.get("/listarpets", include_in_schema=False)
@app.get("/pets", summary="Listar pets")
def listarpets(especie: str | None = Query(default=None, min_length=1, max_length=60)):
    sql = "SELECT id, nome, especie, tutor_id FROM pets"
    parametros = ()
    if especie is not None:
        sql += " WHERE especie = %s"
        parametros = (especie,)
    sql += " ORDER BY id"
    pets = executar_sql(sql, parametros)
    return resposta_didatica(pets, sql, parametros)


@app.get("/consultarpet/{id}", include_in_schema=False)
@app.get("/pets/{id}", summary="Consultar pet por ID")
def consultarpet(id: int = Path(gt=0)):
    sql = "SELECT id, nome, especie, tutor_id FROM pets WHERE id = %s"
    parametros = (id,)
    pets = executar_sql(sql, parametros)
    if not pets:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return resposta_didatica(pets[0], sql, parametros)
