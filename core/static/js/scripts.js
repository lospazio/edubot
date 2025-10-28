// ============================
// Document Ready
// ============================
document.addEventListener("DOMContentLoaded", () => {

    // ============================
    // Chat AI (core/ai_tutor/chat.html)
    // ============================
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    const chatBox = document.querySelector(".chat-box");

    if (chatForm) {
        chatForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const userMessage = chatInput.value.trim();
            if (!userMessage) return;

            // Aggiungi messaggio utente alla chat
            appendMessage("user", userMessage);

            chatInput.value = "";

            // Chiamata API simulata (da sostituire con endpoint reale)
            try {
                const aiResponse = await fakeAIResponse(userMessage);
                appendMessage("ai", aiResponse);
            } catch (err) {
                appendMessage("ai", "Errore nella risposta dell'AI");
                console.error(err);
            }
        });
    }

    function appendMessage(sender, message) {
        const messageEl = document.createElement("div");
        messageEl.classList.add("chat-message", sender);
        const contentEl = document.createElement("div");
        contentEl.classList.add("message-content");
        contentEl.textContent = message;
        messageEl.appendChild(contentEl);
        chatBox.appendChild(messageEl);
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll automatico
    }

    // Simulazione risposta AI (placeholder)
    async function fakeAIResponse(userMessage) {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve("Risposta AI a: " + userMessage);
            }, 1000);
        });
    }

    // ============================
    // Preview file upload (core/notes/upload.html)
    // ============================
    const fileInput = document.getElementById("id_file");
    const filePreview = document.getElementById("file-preview");

    if (fileInput && filePreview) {
        fileInput.addEventListener("change", () => {
            const file = fileInput.files[0];
            if (file) {
                filePreview.textContent = `File selezionato: ${file.name} (${Math.round(file.size / 1024)} KB)`;
            } else {
                filePreview.textContent = "";
            }
        });
    }

    // ============================
    // Toggle menu (se espandi navbar)
    // ============================
    const menuToggle = document.getElementById("menu-toggle");
    const navMenu = document.getElementById("nav-menu");

    if (menuToggle && navMenu) {
        menuToggle.addEventListener("click", () => {
            navMenu.classList.toggle("active");
        });
    }

    // ============================
    // Smooth scroll per anchor link
    // ============================
    const anchors = document.querySelectorAll('a[href^="#"]');
    for (let anchor of anchors) {
        anchor.addEventListener("click", function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute("href")).scrollIntoView({
                behavior: "smooth"
            });
        });
    }

});
