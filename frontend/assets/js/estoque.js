verificarLogin(); 

const API_URL = "https://dummyjson.com/products";
const btnCarregar = document.getElementById("btn-carregar");
const tabela = document.getElementById("tabela-produtos");
const btnSair = document.getElementById("btn-sair");

btnCarregar.addEventListener("click", async () => {
  const resposta = await fetch(API_URL);
  const dados = await resposta.json();

  tabela.innerHTML = "";
  dados.products.forEach(produto => {
    const linha = document.createElement("tr");
    linha.innerHTML = `
      <td>${produto.title}</td>
      <td>R$ ${produto.price.toFixed(2)}</td>
      <td>${produto.stock}</td>
    `;
    tabela.appendChild(linha);
  });
});

// Botão de sair
btnSair.addEventListener("click", () => {
  localStorage.removeItem("logado");
  window.location.href = "../index.html";
});
