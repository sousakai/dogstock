let produtosGlobais = [];
let categoriasGlobais = [];
let ordemAsc = true;

const API_BASE_URL = "http://localhost:8000";
const tabelaProdutos = document.getElementById("tabela-produtos");

let produtoIdParaExcluir = null;
let produtoAtualEdicao = null;

// Referências aos modais
const deleteModal = document.getElementById("deleteModal");
const deleteCloseBtns = deleteModal?.querySelectorAll(".close");
const confirmDelete = document.getElementById("confirmDelete");

const editModal = document.getElementById("editModal");
const editClose = editModal?.querySelectorAll(".close");
const editForm = document.getElementById("editForm");
const cancelEdit = document.getElementById("cancelEdit");

window.onload = async () => {
  await fetchCategorias();
  await fetchProdutos();
  inicializarEventListeners();
};

// ============================
// Inicialização de eventos
// ============================
function inicializarEventListeners() {
  if (confirmDelete) confirmDelete.onclick = confirmarExclusao;
  if (deleteCloseBtns) deleteCloseBtns.forEach((btn) => (btn.onclick = () => (deleteModal.style.display = "none")));
  if (editClose) editClose.forEach((btn) => (btn.onclick = () => (editModal.style.display = "none")));
  if (cancelEdit) cancelEdit.onclick = () => (editModal.style.display = "none");

  window.onclick = (event) => {
    if (event.target === editModal || event.target === deleteModal) {
      editModal.style.display = "none";
      deleteModal.style.display = "none";
    }
  };

  document.querySelectorAll("th[data-col]").forEach((th) => {
    th.addEventListener("click", () => ordenarTabela(th.getAttribute("data-col")));
  });

  const btnExportar = document.getElementById("btn-exportar");
  if (btnExportar) btnExportar.addEventListener("click", exportarPDF);
}

// ============================
// Carregar dados
// ============================
async function fetchProdutos() {
  try {
    showLoading(true);
    const response = await fetch(`${API_BASE_URL}/consulta/produtos/`);
    if (!response.ok) throw new Error(`Erro HTTP: ${response.status}`);

    const data = await response.json();
    produtosGlobais = data;
    localStorage.setItem("produtosGlobais", JSON.stringify(data));

    preencherTabela(produtosGlobais);
  } catch (error) {
    console.error("Erro ao carregar produtos:", error);
    showNotification("Erro ao carregar produtos da API", "error");

    const produtosCache = localStorage.getItem("produtosGlobais");
    if (produtosCache) {
      produtosGlobais = JSON.parse(produtosCache);
      preencherTabela(produtosGlobais);
      showNotification("Carregado do cache local", "info");
    }
  } finally {
    showLoading(false);
  }
}

async function fetchCategorias() {
  try {
    const response = await fetch(`${API_BASE_URL}/consulta/categorias/`);
    if (!response.ok) throw new Error("Erro ao buscar categorias");
    categoriasGlobais = await response.json();
  } catch (error) {
    console.error("Erro ao carregar categorias:", error);
    showNotification("Erro ao carregar categorias", "error");
  }
}

// ============================
// Preencher tabela
// ============================
function preencherTabela(produtos) {
  if (!tabelaProdutos) return;

  tabelaProdutos.innerHTML = "";

  if (!produtos || produtos.length === 0) {
    tabelaProdutos.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:20px;">Nenhum produto encontrado</td></tr>`;
    return;
  }

  produtos.forEach((produto) => {
    const estoque = produto.qtd_disponivel || 0;
    let statusClass = estoque <= 10 ? "vermelho" : estoque <= 50 ? "amarelo" : "verde";

    const categoriaNome =
      categoriasGlobais.find((c) => c.id === produto.categoria_id)?.descricao ||
      `ID ${produto.categoria_id}`;

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${produto.nome || "N/A"}</td>
      <td>R$ ${parseFloat(produto.medida || 0).toFixed(2)}</td>
      <td>${estoque}</td>
      <td>${categoriaNome}</td>
      <td><span class="status ${statusClass}"></span></td>
      <td>
        <a href="#" onclick="abrirModalEdicaoProduto(${produto.id})">
          <img src="../assets/img/draft.png" alt="Editar" width="20">
        </a>
        <a href="#" onclick="excluirProduto(${produto.id})">
          <img src="../assets/img/lixo.png" alt="Excluir" width="20">
        </a>
      </td>
    `;
    tabelaProdutos.appendChild(tr);
  });
}

// ============================
// Excluir produto
// ============================
function excluirProduto(id) {
  produtoIdParaExcluir = id;
  if (deleteModal) deleteModal.style.display = "block";
}

async function confirmarExclusao() {
  if (!produtoIdParaExcluir) return;

  try {
    showLoading(true);
    const response = await fetch(`${API_BASE_URL}/registro/produtos/${produtoIdParaExcluir}`, { method: "DELETE" });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Erro ao excluir produto");
    }

    showNotification("Produto excluído com sucesso!", "success");
    produtosGlobais = produtosGlobais.filter((p) => p.id !== produtoIdParaExcluir);
    preencherTabela(produtosGlobais);
  } catch (error) {
    console.error("Erro ao excluir:", error);
    showNotification(error.message, "error");
  } finally {
    showLoading(false);
    if (deleteModal) deleteModal.style.display = "none";
  }
}

// ============================
// Atualizar produto (PUT)
// ============================
async function atualizarProduto(id, produto) {
  try {
    const response = await fetch(`${API_BASE_URL}/registro/produtos/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(produto),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Erro ao atualizar produto");
    }

    await fetchProdutos();
    return true;
  } catch (error) {
    console.error("Erro ao atualizar produto:", error);
    alert("Erro ao atualizar produto");
    return false;
  }
}

// ============================
// Modal de edição
// ============================
function abrirModalEdicaoProduto(produtoId) {
  produtoAtualEdicao = produtosGlobais.find((p) => p.id === produtoId);

  if (!produtoAtualEdicao) {
    alert("Produto não encontrado!");
    return;
  }

  // Abre o modal
  editModal.style.display = "block";

  // Preenche os campos com os dados existentes
  document.getElementById("editNome").value = produtoAtualEdicao.nome || "";
  document.getElementById("editPreco").value = produtoAtualEdicao.medida || ""; 
  document.getElementById("editEstoque").value = produtoAtualEdicao.qtd_disponivel || "";

  // Popula o select de categorias
  const selectCategoria = document.getElementById("editCategoria");
  if (selectCategoria) {
    selectCategoria.innerHTML = '<option value="">Selecione...</option>';
    categoriasGlobais.forEach((cat) => {
      const option = document.createElement("option");
      option.value = cat.id;
      option.textContent = cat.descricao;
      selectCategoria.appendChild(option);
    });

    // Define a categoria atual
    selectCategoria.value = produtoAtualEdicao.categoria_id || "";
  }

  // Define o evento do botão "Salvar"
  editForm.onsubmit = async (e) => {
    e.preventDefault();

    const nome = document.getElementById("editNome").value.trim();
    const medida = document.getElementById("editPreco").value.trim(); 
    const qtd_disponivel = document.getElementById("editEstoque").value.trim();
    const categoria_id = document.getElementById("editCategoria").value;

    if (!nome || !medida || !qtd_disponivel || !categoria_id) {
      alert("Todos os campos devem ser preenchidos!");
      return;
    }

    if (isNaN(qtd_disponivel) || qtd_disponivel < 0) {
      alert("Quantidade inválida!");
      return;
    }

    const produtoAtualizado = {
      nome,
      medida,
      qtd_disponivel: parseInt(qtd_disponivel),
      qtd_minima: 0,
      categoria_id: parseInt(categoria_id),
      status: produtoAtualEdicao.status || "ativo",
    };

    const sucesso = await atualizarProduto(produtoAtualEdicao.id, produtoAtualizado);
    if (sucesso) editModal.style.display = "none";
  };
}

// ============================
// Exportar PDF
// ============================
function exportarPDF() {
  if (!window.jspdf) {
    showNotification("Biblioteca jsPDF não carregada", "error");
    return;
  }

  try {
    const doc = new window.jspdf.jsPDF();
    const dados = produtosGlobais.map((p) => [
      p.nome || "N/A",
      `R$ ${parseFloat(p.medida || 0).toFixed(2)}`,
      p.qtd_disponivel || 0,
      categoriasGlobais.find((c) => c.id === p.categoria_id)?.descricao || "N/A",
    ]);

    doc.text("Lista de Produtos - DogStock", 14, 15);
    doc.autoTable({
      head: [["Produto", "Preço", "Estoque", "Categoria"]],
      body: dados,
      startY: 25,
      styles: { fontSize: 10 },
      headStyles: { fillColor: [1, 92, 145] },
    });

    doc.save("Produtos_DogStock.pdf");
    showNotification("PDF exportado com sucesso!", "success");
  } catch (error) {
    console.error("Erro ao exportar PDF:", error);
    showNotification("Erro ao exportar PDF", "error");
  }
}

// ============================
// Feedback visual
// ============================
function showLoading(show) {
  let loading = document.getElementById("loading");

  if (!loading) {
    loading = document.createElement("div");
    loading.id = "loading";
    loading.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(loading);
  }

  loading.style.display = show ? "flex" : "none";
}

function showNotification(message, type = "info") {
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.textContent = message;

  document.body.appendChild(toast);
  setTimeout(() => toast.classList.add("show"), 100);
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}
