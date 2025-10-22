const chatContainer = document.getElementById("chatbot-container");
const chatHeader = document.getElementById("chatbot-header");
const chatBody = document.getElementById("chatbot-body");
const chatbox = document.getElementById("chatbox");
const input = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const toggleBtn = document.getElementById("chatbot-toggle");

toggleBtn.onclick = () => {
  chatBody.classList.toggle("hidden");
  const icon = toggleBtn.querySelector("i");
  icon.className = chatBody.classList.contains("hidden")
    ? "fa-solid fa-square"
    : "fa-solid fa-minus";
};

// Exibe mensagem no chat
function addMessage(sender, text) {
  const div = document.createElement("div");
  div.className = sender === "user" ? "msg user" : "msg bot";
  div.innerText = text;
  chatbox.appendChild(div);
  chatbox.scrollTop = chatbox.scrollHeight;
}



// --- PRODUTOS ---
async function carregarProdutosViaChat() {
  addMessage("bot", "🔄 Carregando produtos...");

  try {
    const response = await fetch("https://dummyjson.com/products?limit=25");
    const data = await response.json();
    window.produtosGlobais = data.products;

    // 🔹 salva no localStorage
    localStorage.setItem("produtosGlobais", JSON.stringify(produtosGlobais));

    if (typeof preencherTabela === "function") {
      preencherTabela(produtosGlobais);
    }

    addMessage("bot", `✅ ${produtosGlobais.length} produtos carregados com sucesso!`);
  } catch (error) {
    addMessage("bot", "❌ Erro ao carregar produtos.");
    console.error("Erro:", error);
  }
}


// --- FORNECEDORES ---
async function fetchFornecedores() {
  addMessage("bot", "🔄 Carregando fornecedores locais...");
  await new Promise((r) => setTimeout(r, 500));
  window.fornecedoresGlobais = fornecedoresGlobais || [];

  localStorage.setItem("fornecedoresGlobais", JSON.stringify(fornecedoresGlobais));

  addMessage("bot", `✅ ${fornecedoresGlobais.length} fornecedores disponíveis.`);
}


// --- PROCESSAMENTO DE COMANDOS ---
async function processCommand(text) {
  const command = text.toLowerCase().trim();

  // 🔹 PRODUTOS

   if (command.startsWith("buscar produto")) {
    const termo = command.replace("buscar produto", "").trim();
    if (!termo) {
      addMessage("bot", "Diga o nome do produto. Ex: 'buscar produto perfume'");
      return;
    }

    const resultados = produtosGlobais.filter((p) =>
      Object.values(p).some((val) =>
        String(val).toLowerCase().includes(termo)
      )
    );

    if (resultados.length > 0) {
      addMessage("bot", `🔍 Encontrei ${resultados.length} produto(s):`);
      resultados.slice(0, 5).forEach((p) =>
        addMessage("bot", `${p.title} — R$${p.price} — Estoque: ${p.stock}`)
      );
      if (resultados.length > 5)
        addMessage("bot", "… e mais resultados não exibidos.");
    } else {
      addMessage("bot", "Nenhum produto encontrado com esse termo.");
    }

  } else if (command.includes("estoque baixo")) {
    const baixos = produtosGlobais.filter((p) => p.stock <= 10);
    if (baixos.length > 0) {
      addMessage("bot", "⚠️ Produtos com estoque baixo:");
      baixos.forEach((p) =>
        addMessage("bot", `${p.title} — Apenas ${p.stock} unidades!`)
      );
    } else {
      addMessage("bot", "Tudo certo! Nenhum produto com estoque crítico.");
    }

  // 🔹 FORNECEDORES
  } else if (command.includes("listar fornecedores")) {
    await fetchFornecedores();
    fornecedoresGlobais.forEach((f) =>
      addMessage("bot", `${f.nome} — ${f.contato} — ${f.email}`)
    );

  } else if (command.startsWith("buscar fornecedor")) {
    const termo = command.replace("buscar fornecedor", "").trim();
    if (!termo) {
      addMessage(
        "bot",
        "Digite algo como: 'buscar fornecedor A' ou 'buscar fornecedor 00.000.000/0001-11'"
      );
      return;
    }

    const encontrados = fornecedoresGlobais.filter((f) =>
      Object.values(f).some((val) =>
        String(val).toLowerCase().includes(termo)
      )
    );

    if (encontrados.length > 0) {
      addMessage("bot", `🔍 Encontrei ${encontrados.length} fornecedor(es):`);
      encontrados.forEach((f) =>
        addMessage(
          "bot",
          `${f.nome} — ${f.contato} — ${f.email} — ${f.cnpj}`
        )
      );
    } else {
      addMessage("bot", "Nenhum fornecedor encontrado com esse termo.");
    }

  // 🔹 AJUDA
  } else if (command.includes("ajuda")) {
    addMessage(
      "bot",
      "📘 Comandos disponíveis:\n" +
        "• buscar produto [nome]\n" +
        "• estoque baixo\n" +
        "• listar fornecedores\n" +
        "• buscar fornecedor [nome ou cnpj]\n" +
        "• ajuda"
    );

  } else {
    addMessage("bot", "❓ Não entendi. Digite 'ajuda' para ver os comandos disponíveis.");
  }
}

// Envio de mensagem
sendBtn.onclick = () => {
  const text = input.value.trim();
  if (!text) return;
  addMessage("user", text);
  processCommand(text);
  input.value = "";
};

// Mensagem inicial
document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chatbox");
  const welcomeMessage = `
    <div class="bot-message">
      👋 Olá! Eu sou o assistente do <strong>DogStock</strong> 🐶<br><br>
      Posso ajudar com:<br>
      • <em>"Buscar produto [nome do produto]"</em><br>
      • <em>"Listar fornecedores"</em><br>
      • <em>"Buscar fornecedor [nome do fornecedor]"</em><br>
      • <em>"Mostrar estoque baixo"</em><br>
      • <em>"Ajuda"</em><br><br>
      O que deseja fazer?
    </div>
  `;
  if (chatBox) {
    chatBox.innerHTML += welcomeMessage;
    chatBox.scrollTop = chatBox.scrollHeight;
  }
});
