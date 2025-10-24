let produtosGlobais = []; // armazenar todos
let ordemAsc = true; // controle de ordem

const tabelaProdutos = document.getElementById("tabela-produtos");

// Variável para armazenar o ID do produto a ser excluído
let produtoIdParaExcluir = null;

// Variável para armazenar o produto em edição
let produtoAtualEdicao = null;

// Referências ao modal de exclusão
const deleteModal = document.getElementById("deleteModal");
const deleteCloseBtns = deleteModal.querySelectorAll(".close");
const confirmDelete = document.getElementById("confirmDelete");

// Referências ao modal de edição
const editModal = document.getElementById("editModal");
const editClose = editModal.querySelectorAll(".close");
const editForm = document.getElementById("editForm");
const cancelEdit = document.getElementById("cancelEdit");

window.onload = () => {
  fetchProdutos();
};

// Buscar produtos
async function fetchProdutos() {
  try {
    const response = await fetch("https://dummyjson.com/products?limit=25");
    const data = await response.json();
    produtosGlobais = data.products;
    preencherTabela(produtosGlobais);
  } catch (error) {
    console.error("Erro ao carregar produtos:", error);
  }
}

function preencherTabela(produtos) {
  tabelaProdutos.innerHTML = "";

  if (!produtos || produtos.length === 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="6">Nenhum produto encontrado</td>`;
    tabelaProdutos.appendChild(tr);
    return;
  }

  produtos.forEach((produto) => {
    // lógica para o status
    let statusClass = "verde";
    if (produto.stock <= 10) {
      statusClass = "vermelho";
    } else if (produto.stock <= 50) {
      statusClass = "amarelo";
    }

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${produto.title}</td>
      <td>R$ ${produto.price.toFixed(2)}</td>
      <td>${produto.stock}</td>
      <td>${produto.category}</td>
      <td><span class="status ${statusClass}"></span></td>
      <td>
        <a href="#" onclick="editarProduto(${produto.id})">
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

// Função para abrir o modal de exclusão
function abrirModalExclusao(id) {
  produtoIdParaExcluir = id;
  deleteModal.style.display = "block";
}

// Evento para confirmar a exclusão
confirmDelete.onclick = () => {
  produtosGlobais = produtosGlobais.filter(produto => produto.id !== produtoIdParaExcluir);
  preencherTabela(produtosGlobais);
  deleteModal.style.display = "none";
};

// Fechar o modal de exclusão ao clicar nos botões de fechar ou "Cancelar"
deleteCloseBtns.forEach(btn => {
  btn.onclick = () => {
    deleteModal.style.display = "none";
  };
});

// Função para abrir o modal de edição
function abrirModalEdicao(produtoId) {
  produtoAtualEdicao = produtosGlobais.find(p => p.id === produtoId);

  if (!produtoAtualEdicao) {
    alert("Produto não encontrado!");
    return;
  }

  editModal.style.display = "block";

  document.getElementById("editNome").value = produtoAtualEdicao.title;
  document.getElementById("editPreco").value = produtoAtualEdicao.price;
  document.getElementById("editEstoque").value = produtoAtualEdicao.stock;
  document.getElementById("editCategoria").value = produtoAtualEdicao.category;

  editForm.onsubmit = (e) => {
    e.preventDefault();

    produtoAtualEdicao.title = document.getElementById("editNome").value;
    produtoAtualEdicao.price = parseFloat(document.getElementById("editPreco").value);
    produtoAtualEdicao.stock = parseInt(document.getElementById("editEstoque").value);
    produtoAtualEdicao.category = document.getElementById("editCategoria").value;

    preencherTabela(produtosGlobais);
    editModal.style.display = "none";
  };
}

// Fechar o modal de edição ao clicar no "×" ou "Cancelar"
editClose.forEach(btn => {
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

// Função para excluir produto
async function excluirProduto(id) {
  abrirModalExclusao(id);
}

// Função para editar produto
function editarProduto(id) {
  abrirModalEdicao(id);
}

// Ordenação
document.querySelectorAll("th[data-col]").forEach((th) => {
  th.addEventListener("click", () => {
    const coluna = th.getAttribute("data-col");
    ordemAsc = !ordemAsc;
    produtosGlobais.sort((a, b) => {
      if (a[coluna] < b[coluna]) return ordemAsc ? -1 : 1;
      if (a[coluna] > b[coluna]) return ordemAsc ? 1 : -1;
      return 0;
    });
    preencherTabela(produtosGlobais);
  });
});

// Exportar em PDF
document.getElementById("btn-exportar").addEventListener("click", () => {
  new window.jspdf.jsPDF()
    .autoTable({
      head: [["Produto", "Preço", "Estoque", "Categoria"]],
      body: produtosGlobais.map((p) => [p.title, p.price, p.stock, p.category]),
      startY: 20,
      styles: { fontSize: 12 },
      headStyles: { fillColor: [1, 92, 145] },
    })
    .text("Lista de Produtos", 14, 15)
    .save("Produtos.pdf");
});