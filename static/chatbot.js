document.addEventListener("DOMContentLoaded", async function () {
  const chatBody = document.getElementById("chat-body");
  const chatInput = document.getElementById("chat-input");
  const sendBtn = document.getElementById("send-btn");

  function addMessage(message, isUser) {
    // Check if chatBody exists (good practice)
    if (!chatBody) {
        console.error("Cannot add message: chatBody element not found!");
        return;
    }

    // Create the message bubble element
    const messageDiv = document.createElement("div");

    // Apply CSS class based on who sent the message
    messageDiv.className = isUser ? "user-message" : "bot-message";

    // Set the text content of the message bubble
    messageDiv.textContent = message;

    // Add the message bubble to the chat window
    chatBody.appendChild(messageDiv);

    // Auto-scroll to the bottom to show the latest message
    chatBody.scrollTop = chatBody.scrollHeight;
}

  // Add this function back in:
  async function sendMessageToAPI(message) {
    try {
      const loadingDiv = document.createElement("div");
      loadingDiv.className = "bot-message loading";
      loadingDiv.textContent = "Thinking...";
      chatBody.appendChild(loadingDiv);

      // Make API call to your FastAPI endpoint
      const response = await fetch("http://127.0.0.1:8000/chatbot/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: message }),
      });

      // Remove loading indicator
      chatBody.removeChild(loadingDiv);

      if (response.ok) {
        const data = await response.json();
        // Display the bot's response
        addMessage(data.response, false);
      } else {
        // Handle error
        console.log(`${response}`);
        addMessage("Sorry, I encountered an error. Please try again.", false);
        console.error("API Error:", response.status);
      }
    } catch (error) {
      // Handle network or other errors
      addMessage(
        "Sorry, I couldn't connect to the server. Please check your connection.",
        false
      );
      console.error("Error:", error);
    }
  }

  // Function to process sending a message
  function sendMessage() {
    const message = chatInput.value.trim();
    if (message) {
      // Add user message to chat
      addMessage(message, true);

      // Send to API
      sendMessageToAPI(message);

      // Clear input field
      chatInput.value = "";
    }
  }

  // Handle send button click
  sendBtn.addEventListener("click", function () {
    sendMessage();
  });

  // Handle Enter key press
  chatInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  });
});

