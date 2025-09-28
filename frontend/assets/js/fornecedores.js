let fornecedoresGlobais = [
  { id: 1, nome: "Fornecedor A", contato: "11 99999-1111", email: "a@email.com", cnpj: "00.000.000/0001-11", status: "Ativo" },
  { id: 2, nome: "Fornecedor B", contato: "11 99999-2222", email: "b@email.com", cnpj: "00.000.000/0001-22", status: "Inativo" },
  { id: 3, nome: "Fornecedor C", contato: "11 99999-3333", email: "c@email.com", cnpj: "00.000.000/0001-33", status: "Ativo" }
];

let ordemAsc = true;

function carregarTabela(dados) {
  const tbody = document.getElementById("tabela-fornecedores");
  tbody.innerHTML = "";

  dados.forEach(f => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${f.nome}</td>
      <td>${f.contato}</td>
      <td>${f.email}</td>
      <td>${f.cnpj}</td>
      <td>
        <span class="status ${f.status.toLowerCase()}">${f.status}</span>
      </td>
      <td>
        <a href="#" onclick="editarFornecedor(${f.id})">
          <img src="../assets/img/draft.png" alt="Editar" width="20">
        </a>
        <a href="#" onclick="excluirFornecedor(${f.id})">
          <img src="../assets/img/lixo.png" alt="Excluir" width="20">
        </a>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

// Ordenação ao clicar nos cabeçalhos
document.querySelectorAll("th[data-col]").forEach(th => {
  th.addEventListener("click", () => {
    const coluna = th.getAttribute("data-col");
    ordemAsc = !ordemAsc;
    fornecedoresGlobais.sort((a, b) => {
      if (a[coluna] < b[coluna]) return ordemAsc ? -1 : 1;
      if (a[coluna] > b[coluna]) return ordemAsc ? 1 : -1;
      return 0;
    });
    carregarTabela(fornecedoresGlobais);
  });
});

// Filtro por texto (nome, contato, email ou cnpj)
document.getElementById("filtro").addEventListener("input", (e) => {
  const termo = e.target.value.toLowerCase();
  const filtrados = fornecedoresGlobais.filter(f =>
    f.nome.toLowerCase().includes(termo) ||
    f.contato.toLowerCase().includes(termo) ||
    f.email.toLowerCase().includes(termo) ||
    f.cnpj.toLowerCase().includes(termo)
  );
  carregarTabela(filtrados);
});

// Inicializa tabela
carregarTabela(fornecedoresGlobais);

// Exportar em PDF arrumar a lógica
document.getElementById("btn-exportar").addEventListener("click", () => {
  new window.jspdf.jsPDF()
    .autoTable({
      head: [["Fornecedor", "Contato", "Email", "CNPJ"]],
      body: fornecedoresGlobais.map(p => [p.nome, p.contato, p.email, p.cnpj]),
      startY: 20,
      styles: { fontSize: 12 },
      headStyles: { fillColor: [1, 92, 145] },
    })
    .text("Lista de Fornecedores", 14, 15)
    .save("Fornecedores.pdf");
});



// Funções de ação
function editarFornecedor(id) {
  alert("Editar fornecedor ID: " + id);
}

function excluirFornecedor(id) {
  if (confirm("Deseja realmente excluir este fornecedor?")) {
    fornecedoresGlobais = fornecedoresGlobais.filter(f => f.id !== id);
    carregarTabela(fornecedoresGlobais);
  }
}
