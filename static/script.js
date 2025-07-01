function sendMessage() {
  const messageInput = document.getElementById("message");
  const chatbox = document.getElementById("chatbox");
  const loader = document.getElementById("loader");
  const subject = document.getElementById("subject").value;

  const message = messageInput.value.trim();
  if (!message) return;

  chatbox.innerHTML += `<div class="message"><strong>You:</strong> ${message}</div>`;
  messageInput.value = "";
  loader.style.display = "block";

  fetch("/ask", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ message: message, subject: subject })
  })
  .then(response => response.json())
  .then(data => {
    loader.style.display = "none";
    chatbox.innerHTML += `<div class="message"><strong>AI:</strong> ${data.reply}</div>`;
    chatbox.scrollTop = chatbox.scrollHeight;
  })
  .catch(error => {
    loader.style.display = "none";
    chatbox.innerHTML += `<div class="message"><strong>AI:</strong> Error connecting to server.</div>`;
  });
}
