const API_BASE = "http://127.0.0.1:8000";

// Enable upload button when file is selected
const fileInput = document.getElementById("pdfFile");
const uploadBtn = document.getElementById("uploadBtn");

fileInput.addEventListener("change", function() {
  const file = this.files[0];
  if (file) {
    uploadBtn.disabled = false;
    
    // Update upload label text with filename
    const uploadText = document.querySelector(".upload-text");
    uploadText.textContent = file.name;
  } else {
    uploadBtn.disabled = true;
  }
});

// Upload PDF
async function uploadPDF() {
  const fileInput = document.getElementById("pdfFile");
  const statusDiv = document.getElementById("uploadStatus");

  if (!fileInput.files.length) {
    showStatus(statusDiv, "Please select a PDF first.", "error");
    return;
  }

  const file = fileInput.files[0];
  
  // Validate file type
  if (file.type !== "application/pdf") {
    showStatus(statusDiv, "Please select a valid PDF file.", "error");
    return;
  }

  // Validate file size (50MB max)
  const maxSize = 50 * 1024 * 1024;
  if (file.size > maxSize) {
    showStatus(statusDiv, "File too large. Maximum size is 50MB.", "error");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  showStatus(statusDiv, "Uploading and processing PDF...", "loading");
  uploadBtn.disabled = true;

  try {
    const response = await fetch(`${API_BASE}/upload-pdf`, {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    const data = await response.json();
    showStatus(
      statusDiv,
      `✓ Document processed successfully! ${data.chunks_stored} chunks indexed.`,
      "success"
    );

    // Clear welcome message and enable chat
    const chatMessages = document.getElementById("chatMessages");
    chatMessages.innerHTML = "";
    
    // Add system message
    addMessage(
      "assistant",
      `I've processed your document "${file.name}". You can now ask me questions about its content!`
    );

  } catch (err) {
    console.error("Upload error:", err);
    showStatus(statusDiv, `Upload failed: ${err.message}`, "error");
    uploadBtn.disabled = false;
  }
}

// Ask Question
async function askQuestion() {
  const questionInput = document.getElementById("questionInput");
  const question = questionInput.value.trim();

  if (!question) {
    return;
  }

  // Add user message
  addMessage("user", question);
  questionInput.value = "";

  // Add loading message
  const loadingId = addLoadingMessage();

  try {
    const response = await fetch(`${API_BASE}/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question })
    });

    if (!response.ok) {
      throw new Error(`Request failed: ${response.statusText}`);
    }

    const data = await response.json();

    // Remove loading message
    removeLoadingMessage(loadingId);

    // Add assistant response
    addMessage("assistant", data.answer || "I couldn't find an answer to that question.");

  } catch (err) {
    console.error("Question error:", err);
    removeLoadingMessage(loadingId);
    addMessage(
      "assistant",
      "Sorry, I encountered an error processing your question. Please try again."
    );
  }
}

// Handle Enter key press
function handleKeyPress(event) {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    askQuestion();
  }
}

// Add message to chat
function addMessage(type, content) {
  const chatMessages = document.getElementById("chatMessages");
  const messageDiv = document.createElement("div");
  messageDiv.className = `message message-${type}`;

  if (type === "assistant") {
    messageDiv.innerHTML = `
      <div class="message-avatar">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <div class="message-content">${escapeHtml(content)}</div>
    `;
  } else {
    messageDiv.innerHTML = `
      <div class="message-content">${escapeHtml(content)}</div>
    `;
  }

  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Add loading message
function addLoadingMessage() {
  const chatMessages = document.getElementById("chatMessages");
  const loadingDiv = document.createElement("div");
  const loadingId = `loading-${Date.now()}`;
  loadingDiv.id = loadingId;
  loadingDiv.className = "message message-assistant";
  loadingDiv.innerHTML = `
    <div class="message-avatar">
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    <div class="message-content">
      <div class="loading-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  `;

  chatMessages.appendChild(loadingDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return loadingId;
}

// Remove loading message
function removeLoadingMessage(loadingId) {
  const loadingDiv = document.getElementById(loadingId);
  if (loadingDiv) {
    loadingDiv.remove();
  }
}

// Show status message
function showStatus(element, message, type) {
  element.textContent = message;
  element.className = `status-message ${type}`;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// Handle drag and drop for file upload
const uploadArea = document.getElementById("uploadArea");
const uploadLabel = uploadArea.querySelector(".upload-label");

["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
  uploadArea.addEventListener(eventName, preventDefaults, false);
  document.body.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

["dragenter", "dragover"].forEach(eventName => {
  uploadArea.addEventListener(eventName, () => {
    uploadLabel.style.borderColor = "var(--accent-primary)";
    uploadLabel.style.background = "rgba(0, 212, 255, 0.1)";
  }, false);
});

["dragleave", "drop"].forEach(eventName => {
  uploadArea.addEventListener(eventName, () => {
    uploadLabel.style.borderColor = "var(--border-color)";
    uploadLabel.style.background = "var(--bg-input)";
  }, false);
});

uploadArea.addEventListener("drop", handleDrop, false);

function handleDrop(e) {
  const dt = e.dataTransfer;
  const files = dt.files;

  if (files.length > 0) {
    fileInput.files = files;
    fileInput.dispatchEvent(new Event("change"));
  }
}