const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input") || document.getElementById("userInput");
const chatBox = document.getElementById("chat-box") || document.getElementById("chatbox");

const backendUrl = "http://127.0.0.1:5000"; // Your local Flask backend

chatForm?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = userInput.value.trim();
  if (!message) return;
  appendMessage("You", message);
  userInput.value = "";

  try {
    const res = await fetch(`${backendUrl}/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message })
    });
    const data = await res.json();
    appendMessage("EduTutor", data.response);
  } catch (error) {
    appendMessage("EduTutor", "⚠️ Could not connect to the bot.");
    console.error(error);
  }
});

function appendMessage(sender, text) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message");
  messageDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}


function uploadFile() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];
  if (!file) return;

  appendMessage("You", "📤 Uploading file: " + file.name);

  const formData = new FormData();
  formData.append("file", file);

  fetch(`${backendUrl}/upload`, {
    method: "POST",
    body: formData,
  })
    .then(res => res.json())
    .then(data => {
      appendMessage("EduTutor", data.response || "✅ File processed.");
    })
    .catch(error => {
      appendMessage("EduTutor", "⚠️ File upload failed.");
      console.error(error);
    });
}
