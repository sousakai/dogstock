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

//Funções para deixar as sessões de criar produtos páginaveis
function mostrarSessao(sessao) {
    // Esconde todas
    document.querySelectorAll('.sessao').forEach(div => div.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));

    // Mostra a escolhida
    document.getElementById('sessao-' + sessao).classList.add('active');
    event.target.classList.add('active');
}
