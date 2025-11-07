//Outras funções

const USER_CORRETO = "admin";
const SENHA_CORRETA = "admin123";

// Validação
function validarLogin(usuario, senha) {
  return usuario === USER_CORRETO && senha === SENHA_CORRETA;
}

// Protege páginas (como estoque.html)
function verificarLogin() {
  const logado = localStorage.getItem("logado");
  if (!logado) {
    window.location.href = "../index.html";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const btnSair = document.getElementById("btn-sair");

  if (btnSair) {
    btnSair.addEventListener("click", logout);
  }

  function logout() {
    localStorage.removeItem("logado");
    window.location.href = "../index.html";
  }
});

// Filtro
document.getElementById("filtro").addEventListener("input", (e) => {
  const termo = e.target.value.toLowerCase();
  const filtrados = produtosGlobais.filter(p =>
    p.title.toLowerCase().includes(termo) ||
    p.category.toLowerCase().includes(termo)
  );
  preencherTabela(filtrados);
});


// Adicionar produto (placeholder)
document.getElementById("btn-adicionar").addEventListener("click", () => {
  window.location.href = "novos-produtos.html"; 
});


