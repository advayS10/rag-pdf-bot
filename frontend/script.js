const API_BASE = "http://127.0.0.1:8000";

// Upload PDF
async function uploadPDF() {
  const fileInput = document.getElementById("pdfFile");
  const status = document.getElementById("uploadStatus");

  if (!fileInput.files.length) {
    status.innerText = "Please select a PDF first.";
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  status.innerText = "Uploading PDF...";

  try {
    const response = await fetch(`${API_BASE}/upload-pdf`, {
      method: "POST",
      body: formData
    });

    const data = await response.json();
    status.innerText = `Uploaded successfully. Chunks stored: ${data.chunks_stored}`;
  } catch (err) {
    status.innerText = "Upload failed.";
  }
}

// Ask Question
async function askQuestion() {
  const question = document.getElementById("questionInput").value;
  const answerBox = document.getElementById("answerBox");

  if (!question) {
    answerBox.innerText = "Please enter a question.";
    return;
  }

  answerBox.innerText = "Thinking...";

  try {
    const response = await fetch(`${API_BASE}/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question })
    });

    const data = await response.json();
    answerBox.innerText = data.answer;
  } catch (err) {
    answerBox.innerText = "Error getting answer.";
  }
}
