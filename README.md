# DogStock

Repositório do projeto de Gerenciamento de Estoque desenvolvido para a disciplina de Banco de Dados II, na Universidade Cidade de São Paulo (UNICID). 

**Estado atual:** roda apenas localmente, focado no teste de conexão com o banco de dados remoto.

---

### Como rodar:

Atualmente, o repositório conta com uma página index.html, que faz requisições para a API Python (FastApi), com o objetivo de testar a conexão com o banco de dados PostgreSQL.

Para executar o teste, é necessário possuir o .env.leitura (com as credencias de leitura) e o .env.escrita (com credenciais de escrita). Após realizar o download do repositório, é necessário criar um "venv" e instalar o Uvicorn e todas as dependências necessárias.

Com tudo preparado, execute o comando: 

>**uvicorn main:app --host 0.0.0.0 --port 8000**

para hostear a API localmente.

Importante mencionar que o acesso deve ser feito ao "link" localhost, se acessar direto pelo arquivo HTML, o teste será mal sucedido.

