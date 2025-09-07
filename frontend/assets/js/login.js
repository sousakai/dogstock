const loginForm = document.getElementById("login-form");
const loginErro = document.getElementById("login-erro");

loginForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const usuario = document.getElementById("usuario").value;
  const senha = document.getElementById("senha").value;

  if (validarLogin(usuario, senha)) {
    localStorage.setItem("logado", true);
    window.location.href = "pages/estoque.html";
  } else {
    loginErro.style.display = "block";
  }
});
