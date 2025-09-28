let produtosGlobais = []; // armazenar todos
let ordemAsc = true; // controle de ordem

const tabelaProdutos = document.getElementById('tabela-produtos');

window.onload = () => {
  fetchProdutos();
};

// Buscar produtos
async function fetchProdutos() {
  try {
    const response = await fetch('https://dummyjson.com/products?limit=25');
    const data = await response.json();
    produtosGlobais = data.products; 
    preencherTabela(produtosGlobais);
  } catch (error) {
    console.error('Erro ao carregar produtos:', error);
  }
}

function preencherTabela(produtos) {
  tabelaProdutos.innerHTML = '';

  if (!produtos || produtos.length === 0) {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td colspan="6">Nenhum produto encontrado</td>`;
    tabelaProdutos.appendChild(tr);
    return;
  }

  produtos.forEach(produto => {
    // lógica para o status
    let statusClass = "verde";
    if (produto.stock <= 10) {
      statusClass = "vermelho";
    } else if (produto.stock <= 50) {
      statusClass = "amarelo";
    }

    const tr = document.createElement('tr');
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

// Ordenação
document.querySelectorAll("th[data-col]").forEach(th => {
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

// Exportar em PDF arrumar a lógica
document.getElementById("btn-exportar").addEventListener("click", () => {
  new window.jspdf.jsPDF()
    .autoTable({
      head: [["Produto", "Preço", "Estoque", "Categoria"]],
      body: produtosGlobais.map(p => [p.title, p.price, p.stock, p.category]),
      startY: 20,
      styles: { fontSize: 12 },
      headStyles: { fillColor: [1, 92, 145] },
    })
    .text("Lista de Produtos", 14, 15)
    .save("Produtos.pdf");
});

