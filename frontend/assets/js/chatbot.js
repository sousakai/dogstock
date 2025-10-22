// chatbot.js
const chatContainer = document.getElementById("chatbot-container");
const chatHeader = document.getElementById("chatbot-header");
const chatBody = document.getElementById("chatbot-body");
const chatbox = document.getElementById("chatbox");
const input = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const toggleBtn = document.getElementById("chatbot-toggle");

toggleBtn.onclick = () => {
  chatBody.classList.toggle("hidden");
  toggleBtn.textContent = chatBody.classList.contains("hidden") ? "▢" : "_";
};

function addMessage(sender, text) {
  const div = document.createElement("div");
  div.className = sender === "user" ? "msg user" : "msg bot";
  div.innerText = text;
  chatbox.appendChild(div);
  chatbox.scrollTop = chatbox.scrollHeight;
}

async function processCommand(text) {
  const command = text.toLowerCase();

  if (command.includes("listar produtos")) {
    addMessage("bot", "🗂️ Listando produtos...");
    await fetchProdutos();
    addMessage("bot", "✅ Produtos atualizados na tabela.");
  } else if (command.startsWith("buscar")) {
    const termo = command.replace("buscar", "").trim();
    if (!termo) {
      addMessage("bot", "❗ Diga o nome do produto. Ex: 'buscar perfume'");
      return;
    }

    const resultados = produtosGlobais.filter((p) =>
      p.title.toLowerCase().includes(termo)
    );

    if (resultados.length > 0) {
      addMessage("bot", `🔎 Encontrei ${resultados.length} produto(s):`);
      resultados.forEach((p) =>
        addMessage("bot", `${p.title} — R$${p.price} — Estoque: ${p.stock}`)
      );
    } else {
      addMessage("bot", "Nenhum produto encontrado com esse nome.");
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
  } else if (command.includes("ajuda")) {
    addMessage(
      "bot",
      "📘 Comandos disponíveis:\n- listar produtos\n- buscar [nome]\n- estoque baixo\n- ajuda"
    );
  } else {
    addMessage("bot", "❓ Não entendi. Digite 'ajuda' para ver os comandos.");
  }
}

sendBtn.onclick = () => {
  const text = input.value.trim();
  if (!text) return;
  addMessage("user", text);
  processCommand(text);
  input.value = "";
};

document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chatbox");

  const welcomeMessage = `
    <div class="bot-message">
      👋 Olá! Eu sou o assistente do <strong>DogStock</strong> 🐶<br><br>
      Aqui estão algumas coisas que você pode me pedir:<br>
      • <em>"Listar produtos"</em><br>
      • <em>"Buscar [nome do produto]"</em><br>
      • <em>"Mostrar estoque baixo"</em><br>
      Como posso te ajudar hoje?
    </div>
  `;

  if (chatBox) {
    chatBox.innerHTML += welcomeMessage;
    chatBox.scrollTop = chatBox.scrollHeight; // rola para o final
  }
});
