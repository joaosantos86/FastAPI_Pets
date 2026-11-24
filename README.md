# API de pets e tutores

Um tutor pode ter vários pets. Cada pet pertence a um único tutor, identificado por `pets.tutor_id`. O arquivo `schema.sql` cria a base MySQL `petshop`, as duas tabelas e a chave estrangeira.

## Executar no Windows

1. Com o MySQL Server em execução, abra `schema.sql` no MySQL Workbench e execute o arquivo inteiro para criar a base e as tabelas.
2. Se estiver preparando uma nova instalação, copie `.env.example` para `.env`. Preencha host, porta, usuário e senha do MySQL e defina `DB_NAME=petshop`.
3. Na pasta do projeto, use o PowerShell para instalar as dependências e iniciar a API.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Para carregar dados de exemplo, execute o bloco abaixo uma vez no Workbench.

```sql
USE petshop;
START TRANSACTION;
INSERT INTO tutores (nome, telefone) VALUES ('Ana', '11999990000');
INSERT INTO pets (nome, especie, tutor_id) VALUES ('Luna', 'Gato', LAST_INSERT_ID());
COMMIT;
```

## Conferir no Swagger

Abra <http://127.0.0.1:8000/docs>, selecione uma operação e clique em **Try it out** e **Execute**. Os dois caminhos de cada linha chamam a mesma função.

| Operação | Caminho no Swagger | Caminho do enunciado |
| --- | --- | --- |
| Listar tutores | GET `/tutores` | GET `/listartutores` |
| Listar pets | GET `/pets` | GET `/listarpets` |
| Consultar tutor | GET `/tutores/{id}` | GET `/consultartutor/{id}` |
| Consultar pet | GET `/pets/{id}` | GET `/consultarpet/{id}` |

1. Execute `GET /pets`. A propriedade `dados` contém a lista de pets em ordem de ID. O bloco `didatica` mostra a consulta SQL e os parâmetros enviados ao MySQL.
2. Copie o `id` de um pet para `GET /pets/{id}`. O resultado em `dados` é um objeto. Use o campo `tutor_id` desse pet em `GET /tutores/{id}` para consultar seu tutor.
3. Experimente `GET /pets?especie=Gato`. Confira o trecho `WHERE especie = %s` e o valor `["Gato"]` em `didatica.parametros`. Uma espécie sem correspondências retorna HTTP 200 com `dados` vazio (`[]`).
4. Teste um ID positivo inexistente para receber HTTP 404. Teste `0`, `-1` ou `abc` para receber HTTP 422. Se o Swagger bloquear texto, abra `/pets/abc` diretamente no navegador.
