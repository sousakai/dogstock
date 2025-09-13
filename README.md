# DogStock

Repositório do projeto de Gerenciamento de Estoque desenvolvido para a disciplina de Laboratório de Banco de Dados Avançado (2025/2), na Universidade Cidade de São Paulo (UNICID). 

**Estado atual:** roda apenas localmente, focado no teste de conexão, leitura e escrita com o banco de dados remoto.

**Equipe de desenvolvimento:**
|Nome |Atuação |
|----------------------|-------------|
|[Kayke Gonçalves de Sousa](https://github.com/sousakai) |Backend |
|[Ryahn Paulo Sobral Jesus](https://github.com/RyahnS7)|Backend |
|[Stenio Lucas da Silva Lima](https://github.com/Steniol) |Backend |
|[Bruno Vinicius Chaga de Medeiros Costa](https://github.com/Brunera98)|Frontend |
|[Kauã Lourenço da Silva](https://github.com/KauaLS)|Frontend |
|[Luiz Henrique](https://github.com/luizynhoo)| Frontend|
|[Nina Areal Cezario](https://github.com/ninaareal)| Dados e BI|
---

### Como rodar:

Atualmente, o repositório conta com uma página index.html, que faz requisições para a API Python (FastApi), com o objetivo de testar a conexão com o banco de dados MySQL.

Para executar o teste, é necessário possuir o .env.leitura (com as credencias de leitura) e o .env.escrita (com credenciais de escrita). Após realizar o download do repositório, é necessário criar um "venv" e instalar o Uvicorn e todas as dependências necessárias.

Com tudo preparado, execute o comando: 

>**uvicorn main:app --host 0.0.0.0 --port 8000**

para hostear a API localmente.

Importante mencionar que o acesso deve ser feito ao "link" localhost, se acessar direto pelo arquivo HTML, o teste será mal sucedido.

### Tecnologias Empregadas:

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/amazonwebservices/amazonwebservices-original-wordmark.svg" height="40" width="40 "/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" height="40" width="40 "/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/html5/html5-original-wordmark.svg" height="40" width="40"/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/css3/css3-original-wordmark.svg" height="40" width="40"/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg" height="40" width="40"/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/git/git-original-wordmark.svg" height="40" width="40"/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mysql/mysql-original.svg" height="40" width="40"/>
          
          

---


          
          


