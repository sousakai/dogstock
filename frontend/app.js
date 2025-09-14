// FUNÇÃO PARA TESTAR A CONEXÃO DE CREDENCIAIS COM O BANCO DE DADOS
async function testarConexao() {
  const resultadosDiv = document.getElementById("resultados");
  resultadosDiv.innerHTML = "<p>Carregando...</p>";

  try {
    const response = await fetch("/consulta/teste-banco/");
    if (!response.ok) throw new Error(`Erro HTTP: ${response.status}`);
    
    const data = await response.json();
    resultadosDiv.innerHTML = "";

    const table = document.createElement("table");
    table.classList.add("result-table");
    const header = table.insertRow();
    header.innerHTML = "<th>Ambiente</th><th>Status</th><th>Resultado / Erro</th>";

    for (const env in data) {
      const item = data[env];
      const row = table.insertRow();
      row.insertCell().textContent = env.toUpperCase();
      row.insertCell().textContent = item.status.toUpperCase();
      row.insertCell().textContent = item.status === "ok" ? item.result : item.mensagem;
      if(item.status !== "ok") row.cells[2].style.color = "red";
    }

    resultadosDiv.appendChild(table);

  } catch (err) {
    resultadosDiv.innerHTML = `<p style="color:red;">Erro ao chamar a API: ${err.message}</p>`;
  }
}

// FUNÇÃO GENERICA PARA CRIAR TABELA DE DADOS
function criarTabela(dados, colunas) {
  const table = document.createElement("table");
  table.classList.add("result-table");

  // Cabeçalho
  const thead = table.createTHead();
  const headerRow = thead.insertRow();
  colunas.forEach(col => {
    const th = document.createElement("th");
    th.textContent = col;
    headerRow.appendChild(th);
  });

  // Corpo
  const tbody = table.createTBody();
  dados.forEach(item => {
    const row = tbody.insertRow();
    colunas.forEach(col => {
      const cell = row.insertCell();
      cell.textContent = item[col] !== undefined ? item[col] : "";
    });
  });

  return table;
}

// FUNÇÃO DE CONSULTA NA TABELA CATEGORIAS
async function carregarCategorias() {
  const container = document.getElementById("listaCategorias");
  container.innerHTML = "<p>Carregando...</p>";

  try {
    const res = await fetch("/consulta/categorias/");
    const data = await res.json();
    container.innerHTML = "";

    const colunas = ["id", "descricao"];
    const tabela = criarTabela(data, colunas);
    container.appendChild(tabela);
  } catch (err) {
    container.innerHTML = `<p style="color:red;">Erro ao carregar categorias: ${err}</p>`;
    console.error(err);
  }
}

// FUNÇÃO PARA PRODUTOS
async function carregarProdutos() {
  const container = document.getElementById("listaProdutos");
  container.innerHTML = "<p>Carregando...</p>";

  try {
    const res = await fetch("/consulta/produtos/");
    const data = await res.json();
    container.innerHTML = "";

    const colunas = ["id", "nome", "medida", "qtd_disponivel", "qtd_minima", "categoria_id", "status"];
    const tabela = criarTabela(data, colunas);
    container.appendChild(tabela);
  } catch (err) {
    container.innerHTML = `<p style="color:red;">Erro ao carregar produtos: ${err}</p>`;
    console.error(err);
  }
}

// FUNÇÃO PARA FORNECEDORES
async function carregarFornecedores() {
  const container = document.getElementById("listaFornecedores");
  container.innerHTML = "<p>Carregando...</p>";

  try {
    const res = await fetch("/consulta/fornecedores/");
    const data = await res.json();
    container.innerHTML = "";

    const colunas = ["id", "razao_social", "contato", "email", "cnpj", "status"];
    const tabela = criarTabela(data, colunas);
    container.appendChild(tabela);
  } catch (err) {
    container.innerHTML = `<p style="color:red;">Erro ao carregar fornecedores: ${err}</p>`;
    console.error(err);
  }
}

// FUNÇÃO PARA MOVIMENTAÇÕES
async function carregarMovimentacoes() {
  const container = document.getElementById("listaMovimentacoes");
  container.innerHTML = "<p>Carregando...</p>";

  try {
    const res = await fetch("/consulta/movimentacoes/");
    const data = await res.json();
    container.innerHTML = "";

    const colunas = ["id", "produto_id", "quantidade", "data", "tipo_mov_id", "preco_venda", "preco_compra", "fornecedor_id", "tipo_pag_id"];
    const tabela = criarTabela(data, colunas);
    container.appendChild(tabela);
  } catch (err) {
    container.innerHTML = `<p style="color:red;">Erro ao carregar movimentações: ${err}</p>`;
    console.error(err);
  }
}

// FUNÇÃO PARA TIPOS DE PAGAMENTO
async function carregarTipoPagamento() {
  const container = document.getElementById("listaTipoPag");
  container.innerHTML = "<p>Carregando...</p>";

  try {
    const res = await fetch("/consulta/tipopagamento/");
    const data = await res.json();
    container.innerHTML = "";

    const colunas = ["id", "descricao"];
    const tabela = criarTabela(data, colunas);
    container.appendChild(tabela);
  } catch (err) {
    container.innerHTML = `<p style="color:red;">Erro ao carregar tipos de pagamento: ${err}</p>`;
    console.error(err);
  }
}

// FUNÇÃO PARA TIPOS DE MOVIMENTAÇÃO
async function carregarTipoMovimentacao() {
  const container = document.getElementById("listaTipoMov");
  container.innerHTML = "<p>Carregando...</p>";

  try {
    const res = await fetch("/consulta/tipomovimentacao/");
    const data = await res.json();
    container.innerHTML = "";

    const colunas = ["id", "descricao_mov"];
    const tabela = criarTabela(data, colunas);
    container.appendChild(tabela);
  } catch (err) {
    container.innerHTML = `<p style="color:red;">Erro ao carregar tipos de movimentação: ${err}</p>`;
    console.error(err);
  }
}
