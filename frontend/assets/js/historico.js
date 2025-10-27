const modal = document.getElementById("manualModal");
const btnAbrir = document.getElementById("btnManual");
const btnFechar = document.querySelector(".close");
const btnCancelar = document.getElementById("cancelManual");

btnAbrir.addEventListener("click", () => {
  modal.style.display = "flex"; 
});


btnFechar.addEventListener("click", () => (modal.style.display = "none"));
btnCancelar.addEventListener("click", () => (modal.style.display = "none"));
window.addEventListener("click", (event) => {
  if (event.target === modal) modal.style.display = "none";
});



document.getElementById("btn-exportar").addEventListener("click", () => {
  if (!window.jspdf || !window.jspdf.jsPDF) {
    console.error("Biblioteca jsPDF não carregada corretamente.");
    return;
  }

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();

  const tabela = document.querySelector("#tabela-historico");
  const linhas = tabela.querySelectorAll("tr");


  if (linhas.length === 0) {
    alert("Nenhum dado encontrado na tabela para exportar.");
    return;
  }

  const dados = Array.from(linhas).map((linha) => {
    const colunas = linha.querySelectorAll("td");
    return Array.from(colunas).map((coluna) => coluna.textContent.trim());
  });

  const cabecalho = [["Produto", "Quantidade", "Tp.Pagamento", "Data Saída", "Observações"]];

  doc.text("Histórico de Saídas", 14, 15);
  doc.autoTable({
    head: cabecalho,
    body: dados,
    startY: 20,
    styles: { fontSize: 10 },
    headStyles: { fillColor: [1, 92, 145] },
  });

  doc.save("Historico.pdf");
});


async function carregarHistorico() {
  try {
    const resposta = await fetch("https://suaapi.com/historico"); 
    const dados = await resposta.json();

    const tbody = document.getElementById("tabela-historico");
    tbody.innerHTML = ""; 

    dados.forEach((item) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${item.produto}</td>
        <td>${item.quantidade}</td>
        <td>${item.pagamento}</td>
        <td>${item.dataSaida}</td>
        <td>${item.observacao || "-"}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (erro) {
    console.error("Erro ao carregar histórico:", erro);
  }
}

carregarHistorico();
