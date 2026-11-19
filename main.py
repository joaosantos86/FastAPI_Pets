from fastapi import FastAPI

app = FastAPI(
    title="API de Pets — Projeto Integrador II",
    description=(
        "API REST para gerenciamento de pets e tutores. "
        "Nesta etapa o projeto contém apenas a configuração inicial: "
        "a aplicação FastAPI e a preparação da conexão com o MySQL."
    ),
    version="0.1.0",
)
