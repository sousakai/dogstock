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

document.getElementById("btn-sair").addEventListener("click", logout);

function logout() {
  localStorage.removeItem("logado");
  window.location.href = "../index.html";
}

//Funções para deixar as sessões de criar produtos páginaveis
function mostrarSessao(sessao) {
    // Esconde todas
    document.querySelectorAll('.sessao').forEach(div => div.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    
    // Mostra a escolhida
    document.getElementById('sessao-' + sessao).classList.add('active');
    
    // Marca o botão como ativo
    const btn = document.querySelector(`.tab-btn[onclick="mostrarSessao('${sessao}')"]`);
    if (btn) btn.classList.add('active');
}


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


