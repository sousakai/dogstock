// URL base da API
const API_URL = 'http://localhost:8000'; // Ajuste a porta se necessário

let fornecedoresGlobais = [];
let ordemAsc = true;
let fornecedorIdParaExcluir = null;
let fornecedorAtualEdicao = null;

// Referências aos modais
const deleteModal = document.getElementById("deleteModal");
const deleteCloseBtns = deleteModal.querySelectorAll(".close");
const confirmDelete = document.getElementById("confirmDelete");

const editModal = document.getElementById("editModal");
const editClose = editModal.querySelectorAll(".close");
const editForm = document.getElementById("editForm");
const cancelEdit = document.getElementById("cancelEdit");

// ========== FUNÇÕES DE API ==========

// Buscar todos os fornecedores
async function buscarFornecedores() {
  try {
    const response = await fetch(`${API_URL}/consulta/fornecedores/`);
    if (!response.ok) throw new Error('Erro ao buscar fornecedores');
    const data = await response.json();
    fornecedoresGlobais = data;
    carregarTabela(fornecedoresGlobais);
  } catch (error) {
    console.error('Erro:', error);
    alert('Erro ao carregar fornecedores. Verifique se a API está rodando.');
  }
}

// Criar novo fornecedor
async function criarFornecedor(fornecedor) {
  try {
    const response = await fetch(`${API_URL}/registro/fornecedores/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(fornecedor),
    });
    if (!response.ok) throw new Error('Erro ao criar fornecedor');
    await buscarFornecedores();
    return true;
  } catch (error) {
    console.error('Erro:', error);
    alert('Erro ao criar fornecedor');
    return false;
  }
}

// Atualizar fornecedor
async function atualizarFornecedor(id, fornecedor) {
  try {
    const response = await fetch(`${API_URL}/registro/fornecedores/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(fornecedor),
    });
    if (!response.ok) throw new Error('Erro ao atualizar fornecedor');
    await buscarFornecedores();
    return true;
  } catch (error) {
    console.error('Erro:', error);
    alert('Erro ao atualizar fornecedor');
    return false;
  }
}

// Excluir fornecedor
async function deletarFornecedor(id) {
  try {
    const response = await fetch(`${API_URL}/registro/fornecedores/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Erro ao excluir fornecedor');
    await buscarFornecedores();
    return true;
  } catch (error) {
    console.error('Erro:', error);
    alert('Erro ao excluir fornecedor');
    return false;
  }
}

// ========== FUNÇÕES DE INTERFACE ==========

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
      <td>${f.razao_social}</td>
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
confirmDelete.onclick = async () => {
  const sucesso = await deletarFornecedor(fornecedorIdParaExcluir);
  if (sucesso) {
    deleteModal.style.display = "none";
    alert("Fornecedor excluido com sucesso")
  }
};

// Fechar o modal de exclusão
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

  document.getElementById("editRazaoSocial").value = fornecedorAtualEdicao.razao_social;
  document.getElementById("editContato").value = fornecedorAtualEdicao.contato;
  document.getElementById("editEmail").value = fornecedorAtualEdicao.email;
  document.getElementById("editCnpj").value = fornecedorAtualEdicao.cnpj;

  editForm.onsubmit = async (e) => {
    e.preventDefault();

    const razao_social = document.getElementById("editRazaoSocial").value.trim();
    const contato = document.getElementById("editContato").value.trim();
    const email = document.getElementById("editEmail").value.trim();
    const cnpj = document.getElementById("editCnpj").value.trim();
    const status = fornecedorAtualEdicao.status || "ativo";

    if (!razao_social || !contato || !email || !cnpj) {
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

    const fornecedorAtualizado = { razao_social, contato, email, cnpj, status};
    const sucesso = await atualizarFornecedor(fornecedorAtualEdicao.id, fornecedorAtualizado);
    
    if (sucesso) {
      editModal.style.display = "none";
    }
  };
}

// Fechar o modal de edição
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
      f.razao_social.toLowerCase().includes(termo) ||
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
        f.razao_social,
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

// ========== INICIALIZAÇÃO ==========
window.addEventListener('DOMContentLoaded', () => {
  buscarFornecedores();
});
