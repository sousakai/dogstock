let fornecedoresGlobais = [
  {
    id: 1,
    nome: "Fornecedor A",
    contato: "11 99999-1111",
    email: "a@email.com",
    cnpj: "00.000.000/0001-11",
  },
  {
    id: 2,
    nome: "Fornecedor B",
    contato: "11 99999-2222",
    email: "b@email.com",
    cnpj: "00.000.000/0001-22",
  },
  {
    id: 3,
    nome: "Fornecedor C",
    contato: "11 99999-3333",
    email: "c@email.com",
    cnpj: "00.000.000/0001-33",
  },
];

let ordemAsc = true;

// Variável para armazenar o ID do fornecedor a ser excluído
let fornecedorIdParaExcluir = null;

// Variável para armazenar o fornecedor em edição
let fornecedorAtualEdicao = null;

// Referências ao modal de exclusão
const deleteModal = document.getElementById("deleteModal");
const deleteCloseBtns = deleteModal.querySelectorAll(".close");
const confirmDelete = document.getElementById("confirmDelete");

// Referências ao modal de edição
const editModal = document.getElementById("editModal");
const editClose = editModal.querySelectorAll(".close");
const editForm = document.getElementById("editForm");
const cancelEdit = document.getElementById("cancelEdit");

function carregarTabela(dados) {
  const tbody = document.getElementById("tabela-fornecedores");
  tbody.innerHTML = "";

  if (!dados || dados.length === 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="6">Nenhum fornecedor encontrado</td>`;
    tbody.appendChild(tr);
    return;
  }

  dados.forEach((f) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${f.nome}</td>
      <td>${f.contato}</td>
      <td>${f.email}</td>
      <td>${f.cnpj}</td>
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

// Função para abrir o modal de exclusão
function abrirModalExclusao(id) {
  fornecedorIdParaExcluir = id;
  deleteModal.style.display = "block";
}

// Evento para confirmar a exclusão
confirmDelete.onclick = () => {
  fornecedoresGlobais = fornecedoresGlobais.filter(
    (f) => f.id !== fornecedorIdParaExcluir
  );
  carregarTabela(fornecedoresGlobais);
  deleteModal.style.display = "none";
};

// Fechar o modal de exclusão ao clicar nos botões de fechar ou "Cancelar"
deleteCloseBtns.forEach((btn) => {
  btn.onclick = () => {
    deleteModal.style.display = "none";
  };
});

// Função para abrir o modal de edição
function abrirModalEdicao(fornecedorId) {
  fornecedorAtualEdicao = fornecedoresGlobais.find(
    (f) => f.id === fornecedorId
  );

  if (!fornecedorAtualEdicao) {
    alert("Fornecedor não encontrado!");
    return;
  }

  editModal.style.display = "block";

  document.getElementById("editNome").value = fornecedorAtualEdicao.nome;
  document.getElementById("editContato").value = fornecedorAtualEdicao.contato;
  document.getElementById("editEmail").value = fornecedorAtualEdicao.email;
  document.getElementById("editCnpj").value = fornecedorAtualEdicao.cnpj;

  editForm.onsubmit = (e) => {
    e.preventDefault();

    const nome = document.getElementById("editNome").value.trim();
    const contato = document.getElementById("editContato").value.trim();
    const email = document.getElementById("editEmail").value.trim();
    const cnpj = document.getElementById("editCnpj").value.trim();

    if (!nome || !contato || !email || !cnpj) {
      alert("Todos os campos devem ser preenchidos!");
      return;
    }
    if (!/^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$/.test(cnpj)) {
      alert("CNPJ inválido! Use o formato XX.XXX.XXX/XXXX-XX");
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      alert("E-mail inválido!");
      return;
    }

    fornecedorAtualEdicao.nome = nome;
    fornecedorAtualEdicao.contato = contato;
    fornecedorAtualEdicao.email = email;
    fornecedorAtualEdicao.cnpj = cnpj;

    carregarTabela(fornecedoresGlobais);
    editModal.style.display = "none";
  };
}

// Fechar o modal de edição ao clicar no "×" ou "Cancelar"
editClose.forEach((btn) => {
  btn.onclick = () => {
    editModal.style.display = "none";
  };
});

cancelEdit.onclick = () => {
  editModal.style.display = "none";
};

// Fechar ambos os modais ao clicar fora deles
window.onclick = (event) => {
  if (event.target === editModal || event.target === deleteModal) {
    editModal.style.display = "none";
    deleteModal.style.display = "none";
  }
};

// Evento para filtrar fornecedores
document.getElementById("filtro").addEventListener("input", (e) => {
  const termo = e.target.value.toLowerCase();
  const filtrados = fornecedoresGlobais.filter(
    (f) =>
      f.nome.toLowerCase().includes(termo) ||
      f.contato.toLowerCase().includes(termo) ||
      f.email.toLowerCase().includes(termo) ||
      f.cnpj.toLowerCase().includes(termo)
  );
  carregarTabela(filtrados);
});

// Função para excluir fornecedor
function excluirFornecedor(id) {
  abrirModalExclusao(id);
}

// Função para editar fornecedor
function editarFornecedor(id) {
  abrirModalEdicao(id);
}

// Ordenação
document.querySelectorAll("th[data-col]").forEach((th) => {
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

// Exportar em PDF
document.getElementById("btn-exportar").addEventListener("click", () => {
  new window.jspdf.jsPDF()
    .autoTable({
      head: [["Fornecedor", "Contato", "Email", "CNPJ"]],
      body: fornecedoresGlobais.map((f) => [
        f.nome,
        f.contato,
        f.email,
        f.cnpj,
      ]),
      startY: 20,
      styles: { fontSize: 12 },
      headStyles: { fillColor: [1, 92, 145] },
    })
    .text("Lista de Fornecedores", 14, 15)
    .save("Fornecedores.pdf");
});

// Inicializa tabela
carregarTabela(fornecedoresGlobais);
