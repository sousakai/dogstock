# DogStock

Repositório do projeto de Gerenciamento de Estoque desenvolvido para a disciplina de Laboratório de Banco de Dados Avançado (2025/2), na Universidade Cidade de São Paulo (UNICID). 

**Objetivo:**
A meta da aplicação é oferecer soluções de gestão de estoque, implementando ferramentas de business intelligence para apresentar insights valiosos para a organização. O foco é apoiar pequenas e médias empresas.

**Estado atual:** A aplicação roda com chatbot incluso para pesquisa automatizada de informações, utilizando chamadas de APIs através do Front-end para cadastrar, editar e deletar produtos, movimentações e fornecedores

**Equipe de desenvolvimento:**
|Nome |Atuação | Contato |
|----------------------|-------------|--------|
|[Kayke Gonçalves de Sousa](https://github.com/sousakai) |Backend | [LinkedIn](https://www.linkedin.com/in/kayke-sousa)|
|[Ryahn Paulo Sobral Jesus](https://github.com/RyahnS7)|Backend | [LinkedIn](https://www.linkedin.com/in/ryahn-paulo-664a08286)|
|[Stenio Lucas da Silva Lima](https://github.com/Steniol) |Backend |
|[Kauã Lourenço da Silva](https://github.com/KauaLS)|Frontend | [LinkedIn](https://www.linkedin.com/in/kauã-lourenço-6500302a8)
|[Luiz Henrique](https://github.com/luizynhoo)| Frontend|
|[Bruno Vinicius Chaga de Medeiros Costa](https://github.com/Brunera98)|Dados e BI |
|[Nina Areal Cezario](https://github.com/ninaareal)| Dados e BI| [LinkedIn](https://www.linkedin.com/in/nina-cezario-areal)
---

### Como rodar:

Atualmente, o repositório conta com uma página index.html que permite o login com credenciais "admin" e "admin123". A partir daqui, é possível navegar entre as partes do projeto.

Para executar o teste no banco da aplicação (hospedado em AWS), é necessário possuir o .env.leitura (com as credencias de leitura) e o .env.escrita (com credenciais de escrita). Após realizar o download do repositório, é necessário criar um "venv" e instalar o Uvicorn e todas as dependências necessárias.

Com tudo preparado, execute o comando: 

>**uvicorn main:app --host 0.0.0.0 --port 8000**

para hostear as APIs localmente.

Importante mencionar que o acesso deve ser feito ao "link" localhost, se acessar direto pelo arquivo HTML, o teste será mal sucedido.

### Tecnologias Empregadas:

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/amazonwebservices/amazonwebservices-original-wordmark.svg" height="40" width="40 "/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" height="40" width="40 "/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/html5/html5-original-wordmark.svg" height="40" width="40"/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/css3/css3-original-wordmark.svg" height="40" width="40"/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg" height="40" width="40"/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/git/git-original-wordmark.svg" height="40" width="40"/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mysql/mysql-original.svg" height="40" width="40"/>

          
          


