function sendMessage() {
  const userInput = document.getElementById("user-input").value;
  if (!userInput) return;

  const chatBox = document.getElementById("chat-box");
  const loader = document.getElementById("loader");

  chatBox.innerHTML += `<div><b>You:</b> ${userInput}</div>`;
  loader.style.display = "block"; // Show loader

  fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: userInput })
  })
  .then(response => response.json())
  .then(data => {
    loader.style.display = "none"; // Hide loader
    chatBox.innerHTML += `<div><b>AI:</b> ${data.reply}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
  })
  .catch(error => {
    loader.style.display = "none"; // Hide loader
    chatBox.innerHTML += `<div><b>Error:</b> ${error}</div>`;
  });

  document.getElementById("user-input").value = "";
}
