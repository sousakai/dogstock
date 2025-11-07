// URL base da API
const API_URL = 'http://localhost:8000';

// ========== FUNÇÕES DE NAVEGAÇÃO ==========

function mostrarSessao(nomeSessao) {
  // Remove a classe 'active' de todas as seções e botões
  document.querySelectorAll('.sessao').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));

  // Adiciona 'active' na seção e botão correspondente
  document.getElementById(`sessao-${nomeSessao}`).classList.add('active');
  event.target.classList.add('active');
}

// ========== FUNÇÕES DE API ==========

// Buscar categorias para preencher o select
async function carregarCategorias() {
  try {
    const response = await fetch(`${API_URL}/consulta/categorias/`);
    if (!response.ok) throw new Error('Erro ao buscar categorias');
    const categorias = await response.json();

    const selectCategoria = document.getElementById('categoria');
    selectCategoria.innerHTML = '<option value="">Selecione...</option>';

    categorias.forEach(cat => {
      const option = document.createElement('option');
      option.value = cat.id;
      option.textContent = cat.descricao;
      selectCategoria.appendChild(option);
    });
  } catch (error) {
    console.error('Erro ao carregar categorias:', error);
    alert('Erro ao carregar categorias. Verifique se a API está rodando.');
  }
}

// Criar nova categoria
async function criarCategoria(categoria) {
  try {
    const response = await fetch(`${API_URL}/registro/categoria/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(categoria),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Erro ao criar categoria');
    }

    return await response.json();
  } catch (error) {
    console.error('Erro:', error);
    throw error;
  }
}

// Criar novo produto
async function criarProduto(produto) {
  try {
    const response = await fetch(`${API_URL}/registro/produtos/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(produto),
    });

    // Mostra erro detalhado da API
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Erro ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Erro na API:', error);
    throw error;
  }
}

// Criar novo fornecedor
async function criarFornecedor(fornecedor) {
  try {
    const response = await fetch(`${API_URL}/registro/fornecedores/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(fornecedor),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Erro ao criar fornecedor');
    }

    return await response.json();
  } catch (error) {
    console.error('Erro:', error);
    throw error;
  }
}

// ========== VALIDAÇÕES ==========

function validarCNPJ(cnpj) {
  // Remove caracteres não numéricos
  const cnpjLimpo = cnpj.replace(/[^\d]/g, '');

  if (cnpjLimpo.length !== 14) {
    return false;
  }

  // Validação básica (pode ser melhorada com validação de dígitos verificadores)
  return /^\d{14}$/.test(cnpjLimpo);
}

function formatarCNPJ(valor) {
  // Remove tudo que não é número
  valor = valor.replace(/\D/g, '');

  // Aplica a máscara XX.XXX.XXX/XXXX-XX
  valor = valor.replace(/^(\d{2})(\d)/, '$1.$2');
  valor = valor.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
  valor = valor.replace(/\.(\d{3})(\d)/, '.$1/$2');
  valor = valor.replace(/(\d{4})(\d)/, '$1-$2');

  return valor;
}

function formatarTelefone(valor) {
  // Remove tudo que não é número
  valor = valor.replace(/\D/g, '');

  // Aplica a máscara (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
  if (valor.length <= 10) {
    valor = valor.replace(/^(\d{2})(\d)/g, '($1) $2');
    valor = valor.replace(/(\d)(\d{4})$/, '$1-$2');
  } else {
    valor = valor.replace(/^(\d{2})(\d)/g, '($1) $2');
    valor = valor.replace(/(\d)(\d{4})$/, '$1-$2');
  }

  return valor;
}

// ========== HANDLERS DE FORMULÁRIOS ==========

// Form Categoria
document.getElementById('form-categoria').addEventListener('submit', async (e) => {
  e.preventDefault();

  const nomeCategoria = document.getElementById('nome-categoria').value.trim();

  if (!nomeCategoria) {
    alert('Por favor, preencha o nome da categoria!');
    return;
  }

  try {
    const novaCategoria = {
      descricao: nomeCategoria
    };

    await criarCategoria(novaCategoria);
    alert('✅ Categoria criada com sucesso!');
    document.getElementById('form-categoria').reset();

    await carregarCategorias();
  } catch (error) {
    alert(`❌ Erro ao criar categoria: ${error.message}`);
  }
});

// Form Produto
document.getElementById("form-produto").addEventListener("submit", async (e) => {
  e.preventDefault();

  // Pegando os valores
  const nome = document.getElementById("nome-produto").value.trim();
  const precoInput = document.getElementById("preco").value.trim();
  const qtd_disponivel = parseInt(document.getElementById("estoque").value);
  const categoria_id = parseInt(document.getElementById("categoria").value);
  const status = document.getElementById("status").value; 

  // Validações
  if (!nome || !precoInput || isNaN(qtd_disponivel) || isNaN(categoria_id)) {
    alert("Preencha todos os campos corretamente!");
    return;
  }


  const medida = precoInput.toString();

  const produto = {
    nome,
    medida,               
    qtd_disponivel,
    qtd_minima: 1,        
    categoria_id,
    status,               
  };

  console.log("Enviando para API:", produto); 

  try {
    const resultado = await criarProduto(produto);
    alert("Produto criado com sucesso!");
    console.log("Resposta da API:", resultado);
    e.target.reset();
  } catch (error) {
    alert("Erro: " + error.message);
    console.error(error);
  }
});

// Form Fornecedor
document.getElementById('form-fornecedores').addEventListener('submit', async (e) => {
  e.preventDefault();

  const razao_social = document.getElementById('nome-fornecedor').value.trim();
  const contato = document.getElementById('contato-fornecedor').value.trim();
  const email = document.getElementById('email-fornecedor').value.trim();
  const cnpj = document.getElementById('cnpj-fornecedor').value.trim();
  const status = "ativo"

  if (!razao_social || !contato || !email || !cnpj) {
    alert('Por favor, preencha todos os campos!');
    return;
  }

  // Validação de e-mail
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    alert('E-mail inválido!');
    return;
  }

  // Validação de CNPJ
  if (!validarCNPJ(cnpj)) {
    alert('CNPJ inválido! Use o formato XX.XXX.XXX/XXXX-XX');
    return;
  }

  const novoFornecedor = {
    razao_social: razao_social,
    contato: contato,
    email: email,
    cnpj: cnpj,
    status: status
  };

  try {
    const fornecedorCriado =
      await criarFornecedor(novoFornecedor);
    alert('✅ Fornecedor criado com sucesso!');
    document.getElementById('form-fornecedores').reset();
  } catch (error) {
    alert(`❌ Erro ao criar fornecedor: ${error.message}`);
  }
});

// ========== MÁSCARAS DE INPUT ==========

// Máscara para CNPJ
document.getElementById('cnpj-fornecedor').addEventListener('input', (e) => {
  e.target.value = formatarCNPJ(e.target.value);
});

// Máscara para Telefone
document.getElementById('contato-fornecedor').addEventListener('input', (e) => {
  e.target.value = formatarTelefone(e.target.value);
});

// Limitar preço a 2 casas decimais
document.getElementById('preco').addEventListener('blur', (e) => {
  if (e.target.value) {
    e.target.value = parseFloat(e.target.value).toFixed(2);
  }
});

// ========== BOTÃO SAIR ==========

document.getElementById('btn-sair').addEventListener('click', () => {
  if (confirm('Deseja realmente sair?')) {
    window.location.href = '../index.html'; // Ajuste o caminho conforme necessário
  }
});

// ========== INICIALIZAÇÃO ==========

window.addEventListener('DOMContentLoaded', async () => {
  // Carrega as categorias quando a página é carregada
  await carregarCategorias();
});