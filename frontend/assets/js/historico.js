// URL base da API
const API_URL = 'http://localhost:8000';

// Referências ao modal
const modal = document.getElementById("manualModal");
const btnAbrir = document.getElementById("btnManual");
const btnFechar = document.querySelector(".close");
const btnCancelar = document.getElementById("cancelManual");
const manualForm = document.getElementById("manualForm");

// Cache de dados para melhor performance
let produtosCache = [];
let tiposPagamentoCache = [];

// ========== FUNÇÕES DE API ==========

// Buscar todos os produtos
async function buscarProdutos() {
  try {
    const response = await fetch(`${API_URL}/consulta/produtos/`);
    if (!response.ok) throw new Error('Erro ao buscar produtos');
    produtosCache = await response.json();
    return produtosCache;
  } catch (error) {
    console.error('Erro ao buscar produtos:', error);
    return [];
  }
}

// Buscar tipos de pagamento
async function buscarTiposPagamento() {
  try {
    const response = await fetch(`${API_URL}/consulta/tipopagamento/`);
    if (!response.ok) throw new Error('Erro ao buscar tipos de pagamento');
    tiposPagamentoCache = await response.json();
    return tiposPagamentoCache;
  } catch (error) {
    console.error('Erro ao buscar tipos de pagamento:', error);
    return [];
  }
}

// Buscar movimentações
async function buscarMovimentacoes() {
  try {
    const response = await fetch(`${API_URL}/consulta/movimentacoes/`);
    if (!response.ok) throw new Error('Erro ao buscar movimentações');
    return await response.json();
  } catch (error) {
    console.error('Erro ao buscar movimentações:', error);
    return [];
  }
}

// Criar nova movimentação
async function criarMovimentacao(movimentacao) {
  try {
    const response = await fetch(`${API_URL}/registro/movimentacoes/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(movimentacao),
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Erro ao criar movimentação');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Erro:', error);
    throw error;
  }
}

// ========== FUNÇÕES DE MAPEAMENTO ==========

// Buscar nome do produto por ID
function getNomeProduto(produtoId) {
  const produto = produtosCache.find(p => p.id === produtoId);
  return produto ? produto.nome : `Produto #${produtoId}`;
}

// Buscar nome do tipo de pagamento por ID
function getNomeTipoPagamento(tipoId) {
  const tipo = tiposPagamentoCache.find(t => t.id === tipoId);
  return tipo ? tipo.nome : '-';
}

// ========== CARREGAR E EXIBIR HISTÓRICO ==========

async function carregarHistorico() {
  try {
    // Busca todos os dados necessários
    const [movimentacoes, produtos, tiposPagamento] = await Promise.all([
      buscarMovimentacoes(),
      buscarProdutos(),
      buscarTiposPagamento()
    ]);

    const tbody = document.getElementById("tabela-historico");
    tbody.innerHTML = "";

    if (!movimentacoes || movimentacoes.length === 0) {
      tbody.innerHTML = '<tr><td colspan="5">Nenhuma movimentação encontrada</td></tr>';
      return;
    }

    // Ordena por data (mais recentes primeiro)
    movimentacoes.sort((a, b) => new Date(b.data) - new Date(a.data));

    movimentacoes.forEach((item) => {
      const tr = document.createElement("tr");
      
      const nomeProduto = getNomeProduto(item.produto_id);
      const preco_compra = item.preco_compra ? `R$ ${item.preco_compra.toFixed(2)}` : '-';
      const dataFormatada = new Date(item.data).toLocaleDateString('pt-BR');
      const observacoes = item.observacoes || '-';

      tr.innerHTML = `
        <td>${nomeProduto}</td>
        <td>${item.quantidade}</td>
        <td>${preco_compra}</td>
        <td>${dataFormatada}</td>
        <td>${observacoes}</td>
      `;
      tbody.appendChild(tr);
    });

  } catch (erro) {
    console.error("Erro ao carregar histórico:", erro);
    alert('Erro ao carregar histórico. Verifique se a API está rodando.');
  }
}

// ========== POPULAR SELECTS DO MODAL ==========

async function popularSelectProdutos() {
  const select = document.getElementById('manualProduto');
  select.innerHTML = '<option value="">Selecione um produto...</option>';
  
  const produtos = await buscarProdutos();
  produtos.forEach(produto => {
    const option = document.createElement('option');
    option.value = produto.id;
    option.textContent = `${produto.nome} (Estoque: ${produto.estoque})`;
    select.appendChild(option);
  });
}

async function popularSelectPagamento() {
  const select = document.getElementById('manualPagamento');
  select.innerHTML = '<option value="">Selecione...</option>';
  
  const tiposPagamento = await buscarTiposPagamento();
  
  if (tiposPagamento.length === 0) {
    // Fallback com opções padrão se a API não retornar dados
    const opcoesPadrao = [
      { id: 1, nome: 'Dinheiro' },
      { id: 2, nome: 'Cartão' },
      { id: 3, nome: 'PIX' }
    ];
    opcoesPadrao.forEach(tipo => {
      const option = document.createElement('option');
      option.value = tipo.id;
      option.textContent = tipo.nome;
      select.appendChild(option);
    });
  } else {
    tiposPagamento.forEach(tipo => {
      const option = document.createElement('option');
      option.value = tipo.id;
      option.textContent = tipo.nome;
      select.appendChild(option);
    });
  }
}

// ========== CONTROLES DO MODAL ==========

btnAbrir.addEventListener("click", async () => {
  await popularSelectProdutos();
  await popularSelectPagamento();
  
  // Define a data atual como padrão
  const hoje = new Date().toISOString().split('T')[0];
  document.getElementById('manualData').value = hoje;
  
  modal.style.display = "flex";
});


btnFechar.addEventListener("click", () => {
  modal.style.display = "none";
  manualForm.reset();
});

btnCancelar.addEventListener("click", () => {
  modal.style.display = "none";
  manualForm.reset();
});

window.addEventListener("click", (event) => {
  if (event.target === modal) {
    modal.style.display = "none";
    manualForm.reset();
  }
});

// ========== SUBMIT DO FORMULÁRIO ==========

manualForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const produtoId = parseInt(document.getElementById('manualProduto').value);
  const quantidade = parseInt(document.getElementById('manualQuantidade').value);
  const data = document.getElementById('manualData').value;
  const preco_compra = parseInt(document.getElementById('manualPagamento').value);
  
  if (!produtoId || !quantidade || !data || !preco_compra) {
    alert('Por favor, preencha todos os campos!');
    return;
  }
  
  if (quantidade <= 0) {
    alert('A quantidade deve ser maior que zero!');
    return;
  }
  
  // Verifica se há estoque suficiente
  const produto = produtosCache.find(p => p.id === produtoId);
  if (produto && produto.estoque < quantidade) {
    if (!confirm(`Atenção! O estoque atual é ${produto.estoque}. Deseja continuar mesmo assim?`)) {
      return;
    }
  }
  
  try {
    const novaMovimentacao = {
      produto_id: produtoId,
      quantidade: quantidade,
      data: data,
      tipo_mov_id: 2, 
      fornecedor_id: 0, 
      tipo_pag_id: tipoPagId,
      preco_compra: 0, 
      preco_venda: produto ? produto.preco : 0
    };
    
    await criarMovimentacao(novaMovimentacao);
    alert('✅ Movimentação registrada com sucesso!');
    
    modal.style.display = "none";
    manualForm.reset();
    
    // Recarrega o histórico
    await carregarHistorico();
    
  } catch (error) {
    alert(`❌ Erro ao registrar movimentação: ${error.message}`);
  }
});

// ========== EXPORTAR PDF ==========

document.getElementById("btn-exportar").addEventListener("click", () => {
  if (!window.jspdf || !window.jspdf.jsPDF) {
    console.error("Biblioteca jsPDF não carregada corretamente.");
    alert("Erro ao carregar biblioteca de PDF.");
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

  const cabecalho = [["Produto", "Quantidade", "Valor", "Data Saída", "Observações"]];

  doc.text("Histórico de Saídas", 14, 15);
  doc.autoTable({
    head: cabecalho,
    body: dados,
    startY: 20,
    styles: { fontSize: 10 },
    headStyles: { fillColor: [1, 92, 145] },
  });

  const dataAtual = new Date().toLocaleDateString('pt-BR').replace(/\//g, '-');
  doc.save(`Historico_${dataAtual}.pdf`);
});

// ========== BOTÃO SAIR ==========

document.getElementById('btn-sair').addEventListener('click', () => {
  if (confirm('Deseja realmente sair?')) {
    window.location.href = '../index.html';
  }
});

// ========== INICIALIZAÇÃO ==========

window.addEventListener('DOMContentLoaded', async () => {
  await carregarHistorico();
});