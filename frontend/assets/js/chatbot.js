// chatbot.js - Conectado à API real do DogStock
const chatContainer = document.getElementById("chatbot-container");
const chatHeader = document.getElementById("chatbot-header");
const chatBody = document.getElementById("chatbot-body");
const chatbox = document.getElementById("chatbox");
const input = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const toggleBtn = document.getElementById("chatbot-toggle");

// ✅ Constante exclusiva para evitar conflito com outras telas
const CHATBOT_API_BASE = "http://localhost:8000";

// CONTROLE DO CHATBOT
if (toggleBtn) {
  toggleBtn.onclick = () => {
    chatBody.classList.toggle("hidden");
    const icon = toggleBtn.querySelector("i");
    icon.className = chatBody.classList.contains("hidden")
      ? "fa-solid fa-square"
      : "fa-solid fa-minus";
  };
}

function addMessage(sender, text) {
  const div = document.createElement("div");
  div.className = sender === "user" ? "msg user" : "msg bot";
  div.innerText = text;
  chatbox.appendChild(div);
  chatbox.scrollTop = chatbox.scrollHeight;
}

// CARREGAR PRODUTOS DA API
async function carregarProdutosViaChat() {
  addMessage("bot", "🔄 Carregando produtos...");

  try {
    const response = await fetch(`${CHATBOT_API_BASE}/consulta/produtos/`);
    if (!response.ok) throw new Error(`Erro HTTP: ${response.status}`);

    const produtos = await response.json();
    window.produtosGlobais = produtos;
    localStorage.setItem("produtosGlobais", JSON.stringify(produtos));

    if (typeof preencherTabela === "function") preencherTabela(produtos);

    addMessage("bot", `✅ ${produtos.length} produtos carregados com sucesso!`);
    return produtos;
  } catch (error) {
    addMessage("bot", "❌ Erro ao carregar produtos da API.");
    console.error("Erro:", error);
    return [];
  }
}

// CARREGAR FORNECEDORES DA API
async function fetchFornecedores() {
  addMessage("bot", "🔄 Carregando fornecedores...");

  try {
    const response = await fetch(`${CHATBOT_API_BASE}/consulta/fornecedores/`);
    if (!response.ok) throw new Error(`Erro HTTP: ${response.status}`);

    const fornecedores = await response.json();
    window.fornecedoresGlobais = fornecedores;
    localStorage.setItem("fornecedoresGlobais", JSON.stringify(fornecedores));

    addMessage("bot", `✅ ${fornecedores.length} fornecedores carregados!`);
    return fornecedores;
  } catch (error) {
    addMessage("bot", "❌ Erro ao carregar fornecedores da API.");
    console.error("Erro:", error);
    return [];
  }
}

// CARREGAR CATEGORIAS DA API
async function carregarCategorias() {
  addMessage("bot", "🔄 Carregando categorias...");

  try {
    const response = await fetch(`${CHATBOT_API_BASE}/consulta/categorias/`);
    const categorias = await response.json();

    addMessage("bot", `✅ ${categorias.length} categorias disponíveis!`);
    return categorias;
  } catch (error) {
    addMessage("bot", "❌ Erro ao carregar categorias.");
    console.error("Erro:", error);
    return [];
  }
}

// PROCESSAR COMANDOS
async function processCommand(text) {
  const command = text.toLowerCase().trim();

  // BUSCAR PRODUTO
  if (command.startsWith("buscar produto")) {
    const termo = command.replace("buscar produto", "").trim();
    if (!termo) {
      addMessage(
        "bot",
        "💡 Diga o nome do produto. Ex: 'buscar produto ração'"
      );
      return;
    }

    try {
      const response = await fetch(`${CHATBOT_API_BASE}/consulta/produtos/`);
      const produtos = await response.json();

      const resultados = produtos.filter((p) =>
        Object.values(p).some((val) =>
          String(val).toLowerCase().includes(termo)
        )
      );

      if (resultados.length > 0) {
        addMessage("bot", `🔍 Encontrei ${resultados.length} produto(s):`);
        resultados.slice(0, 5).forEach((p) => {
          const nome = p.nome || p.title || "Sem nome";
          const medida = p.medida || p.price || 0;
          const qtd_disponivel = p.qtd_disponivel || p.stock || 0;
          addMessage(
            "bot",
            `${nome} — R$${parseFloat(medida).toFixed(
              3
            )} — Estoque: ${qtd_disponivel}`
          );
        });
        if (resultados.length > 5)
          addMessage("bot", `… e mais ${resultados.length - 5} produtos.`);
      } else {
        addMessage("bot", "❌ Nenhum produto encontrado com esse termo.");
      }
    } catch (error) {
      addMessage("bot", "❌ Erro ao buscar produtos.");
      console.error("Erro:", error);
    }

    //  CARREGAR PRODUTOS
  } else if (command.includes("carregar produtos")) {
    await carregarProdutosViaChat();

    // ESTOQUE BAIXO
  } else if (command.includes("estoque baixo")) {
    try {
      const response = await fetch(`${CHATBOT_API_BASE}/consulta/produtos/`);
      const produtos = await response.json();

      const baixos = produtos.filter(
        (p) => (p.qtd_disponivel || p.stock || 0) <= 10
      );

      if (baixos.length > 0) {
        addMessage("bot", `⚠️ ${baixos.length} produto(s) com estoque baixo:`);
        baixos.slice(0, 10).forEach((p) => {
          const nome = p.nome || p.title || "Sem nome";
          const estoque = p.qtd_disponivel || p.stock || 0;
          addMessage("bot", `${nome} — Apenas ${estoque} unidades!`);
        });
        if (baixos.length > 10)
          addMessage("bot", `... e mais ${baixos.length - 10} produtos.`);
      } else {
        addMessage("bot", "✅ Tudo certo! Nenhum produto com estoque crítico.");
      }
    } catch (error) {
      addMessage("bot", "❌ Erro ao verificar estoque.");
      console.error("Erro:", error);
    }

    // LISTAR FORNECEDORES
  } else if (command.includes("listar fornecedores")) {
    const fornecedores = await fetchFornecedores();
    if (fornecedores.length > 0) {
      fornecedores.slice(0, 10).forEach((f) => {
        const nome = f.razao_social || f.nome_fornecedor || "Sem nome";
        const contato = f.contato || f.telefone || "N/A";
        const email = f.email || "N/A";
        addMessage("bot", `${nome} — ${contato} — ${email}`);
      });
      if (fornecedores.length > 10)
        addMessage(
          "bot",
          `... e mais ${fornecedores.length - 10} fornecedores.`
        );
    }

    // BUSCAR FORNECEDOR
  } else if (command.startsWith("buscar fornecedor")) {
    const termo = command.replace("buscar fornecedor", "").trim();
    if (!termo) {
      addMessage("bot", "💡 Digite: 'buscar fornecedor [nome ou CNPJ]'");
      return;
    }

    try {
      const response = await fetch(
        `${CHATBOT_API_BASE}/consulta/fornecedores/`
      );
      const fornecedores = await response.json();

      const encontrados = fornecedores.filter((f) =>
        Object.values(f).some((val) =>
          String(val).toLowerCase().includes(termo)
        )
      );

      if (encontrados.length > 0) {
        addMessage("bot", `🔍 Encontrei ${encontrados.length} fornecedor(es):`);
        encontrados.forEach((f) => {
          const nome = f.razao_social || f.nome_fornecedor || "Sem nome";
          const contato = f.contato || f.telefone || "N/A";
          const email = f.email || "N/A";
          const cnpj = f.cnpj || "N/A";
          addMessage("bot", `${nome} — ${contato} — ${email} — ${cnpj}`);
        });
      } else {
        addMessage("bot", "❌ Nenhum fornecedor encontrado.");
      }
    } catch (error) {
      addMessage("bot", "❌ Erro ao buscar fornecedores.");
      console.error("Erro:", error);
    }

    // AJUDA
  } else if (command.includes("ajuda") || command === "help") {
    addMessage(
      "bot",
      "📘 Comandos disponíveis:\n\n" +
        "• buscar produto [nome]\n" +
        "• carregar produtos\n" +
        "• estoque baixo\n" +
        "• listar fornecedores\n" +
        "• buscar fornecedor [nome ou cnpj]\n" +
        "• ajuda"
    );

    // COMANDO NÃO RECONHECIDO
  } else {
    addMessage(
      "bot",
      "❓ Não entendi. Digite 'ajuda' para ver os comandos disponíveis."
    );
  }
}

// EVENT LISTENERS
if (sendBtn) {
  sendBtn.onclick = () => {
    const text = input.value.trim();
    if (!text) return;
    addMessage("user", text);
    processCommand(text);
    input.value = "";
  };
}

if (input) {
  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendBtn.click();
  });
}

// MENSAGEM INICIAL
document.addEventListener("DOMContentLoaded", () => {
  if (!chatbox) return;

  const welcomeMessage = `
    <div class="bot-message">
      👋 Olá! Eu sou o assistente do <strong>DogStock</strong> 🐶<br><br>
      Posso ajudar com:<br>
      • <em>"Buscar produto [nome]"</em><br>
      • <em>"Carregar produtos"</em><br>
      • <em>"Estoque baixo"</em><br>
      • <em>"Listar fornecedores"</em><br>
      • <em>"Buscar fornecedor [nome]"</em><br>
      • <em>"Ajuda"</em><br><br>
      O que deseja fazer?
    </div>
  `;

  chatbox.innerHTML += welcomeMessage;
  chatbox.scrollTop = chatbox.scrollHeight;
});
