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
      li.textContent = `${cat.id} - ${cat.descricao}`;
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

    const categorias = Array.isArray(data) ? data : Object.values(data);

    lista.innerHTML = "";

    categorias.forEach(cat => {
      const li = document.createElement("li");
      li.textContent = `${cat.id} - ${cat.nome} - ${cat.medida} - ${cat.qtd_disponivel} - ${cat.qtd_minima} - ${cat.categoria_id} - ${cat.status}`;
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
});
