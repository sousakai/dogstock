//Lógica dos produtos

const tabelaProdutos = document.getElementById('tabela-produtos');

window.onload = function(){
    fetchProdutos()
}

async function fetchProdutos() {
  try {
    const response = await fetch('https://dummyjson.com/products?limit=25');
    const data = await response.json();

    preencherTabela(data.products); 
  } catch (error) {
    console.error('Erro ao carregar produtos:', error);
  }
}

function preencherTabela(produtos) {
  tabelaProdutos.innerHTML = '';

  if (produtos.length === 0) {
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
