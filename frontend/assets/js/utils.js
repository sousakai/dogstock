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

