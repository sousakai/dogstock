// FUNÇÃO PARA TESTAR A CONEXÃO DE CREDENCIAIS COM O BANCO DE DADOS
async function testarConexao() {
  const resultadosDiv = document.getElementById("resultados");
  resultadosDiv.innerHTML = "<p>Carregando...</p>";

  try {
    const response = await fetch("/teste-db"); // endpoint da API
    if (!response.ok) throw new Error(`Erro HTTP: ${response.status}`);
    
    const data = await response.json();
    resultadosDiv.innerHTML = "";

    for (const env in data) {
      const item = data[env];
      const div = document.createElement("div");
      div.classList.add("env-result");
      div.classList.add(item.status === "ok" ? "ok" : "erro");

      div.innerHTML = `<strong>${env.toUpperCase()}</strong> - Status: ${item.status.toUpperCase()}`;
      if (item.status === "erro") {
        const pre = document.createElement("pre");
        pre.textContent = item.mensagem;
        div.appendChild(pre);
      } else {
        div.innerHTML += ` - Result: ${item.result}`;
      }

      resultadosDiv.appendChild(div);
    }

  } catch (err) {
    resultadosDiv.innerHTML = `<p style="color:red;">Erro ao chamar a API: ${err.message}</p>`;
  }
}

// FUNÇÃO DE CONSULTA NA TABELA CATEGORIAS
async function carregarCategorias() {
  const lista = document.getElementById("listaCategorias");
  lista.innerHTML = "<li>Carregando...</li>";

  try {
    const res = await fetch("/categorias"); // router da api backend
    const data = await res.json();
    console.log("Retorno da API:", data);

    const categorias = Array.isArray(data) ? data : Object.values(data);

    lista.innerHTML = "";

    categorias.forEach(cat => {
      const li = document.createElement("li");
      li.textContent = 
        `${cat.id} - 
        ${cat.descricao}`;
      lista.appendChild(li);
    });
  } catch (err) {
    lista.innerHTML = `<li>Erro ao carregar categorias: ${err}</li>`;
    console.error(err);
  }
}

// FUNÇÃO PARA CONSULTAR OS PRODUTOS - TABELA PRODUTOS
async function carregarProdutos() {
  const lista = document.getElementById("listaProdutos");
  lista.innerHTML = "<li>Carregando...</li>";

  try {
    const res = await fetch("/produtos"); // router da api backend
    const data = await res.json();
    console.log("Retorno da API:", data);

    const produtos = Array.isArray(data) ? data : Object.values(data);

    lista.innerHTML = "";

    produtos.forEach(prod => {
      const li = document.createElement("li");
      li.textContent = 
        `${prod.id} - 
        ${prod.nome} - 
        ${prod.medida} - 
        ${prod.qtd_disponivel} - 
        ${prod.qtd_minima} - 
        ${prod.categoria_id} - 
        ${prod.status}`;
      lista.appendChild(li);
    });
  } catch (err) {
    lista.innerHTML = `<li>Erro ao carregar Produtos: ${err}</li>`;
    console.error(err);
  }
}


// FUNÇÃO PARA LISTAR FORNECEDORES - TABELA FORNECEDORES
async function carregarFornecedores() {
  const lista = document.getElementById("listaFornecedores");
  lista.innerHTML = "<li>Carregando...</li>";

  try {
    const res = await fetch("/fornecedores"); // router da api backend
    const data = await res.json();
    console.log("Retorno da API:", data);

    const fornecedores = Array.isArray(data) ? data : Object.values(data);

    lista.innerHTML = "";

    fornecedores.forEach(forn => {
      const li = document.createElement("li");
      li.textContent = 
        `${forn.id} - 
        ${forn.nome} - 
        ${forn.contato} - 
        ${forn.email} - 
        ${forn.cnpj} - 
        ${forn.status}`;
      lista.appendChild(li);
    });
  } catch (err) {
    lista.innerHTML = `<li>Erro ao carregar Produtos: ${err}</li>`;
    console.error(err);
  }
}

// FUNÇÃO PARA CONSULTAR MOVIMENTACOES - TABELA MOVIMENTACOES
async function carregarMovimentacoes() {
  const lista = document.getElementById("listaMovimentacoes");
  lista.innerHTML = "<li>Carregando...</li>";

  try {
    const res = await fetch("/movimentacoes"); // router da api backend
    const data = await res.json();
    console.log("Retorno da API:", data);

    const movimentacoes= Array.isArray(data) ? data : Object.values(data);

    lista.innerHTML = "";

    movimentacoes.forEach(mov => {
      const li = document.createElement("li");
      li.textContent = 
        `${mov.id} - 
        ${mov.produto_id} - 
        ${mov.quantidade} - 
        ${mov.data} - 
        ${mov.tipo_mov_id} - 
        ${mov.preco_venda} -
        ${mov.preco_compra} - 
        ${mov.fornecedor_id} - 
        ${mov.tipo_pag_id}`;
      lista.appendChild(li);
    });
  } catch (err) {
    lista.innerHTML = `<li>Erro ao carregar Produtos: ${err}</li>`;
    console.error(err);
  }
}

// Roda as duas funções ao carregar a página
document.addEventListener("DOMContentLoaded", () => {
  carregarCategorias();
  testarConexao();
  carregarProdutos();
  carregarFornecedores();
  carregarMovimentacoes();
});
