const classifyBtn = document.getElementById("classifyBtn");
const messagesInput = document.getElementById("messages");
const resultsDiv = document.getElementById("results");
const loading = document.getElementById("loading");

const API_URL = "http://localhost:8000/classify";

classifyBtn.addEventListener("click", async () => {

  const rawMessages = messagesInput.value
    .split("\n")
    .map(msg => msg.trim())
    .filter(msg => msg.length > 0);

  if (rawMessages.length === 0) {
    alert("Please enter at least one support message.");
    return;
  }

  resultsDiv.innerHTML = "";
  loading.classList.remove("hidden");

  try {

    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        messages: rawMessages
      })
    });

    if (!response.ok) {
      throw new Error("Failed to classify tickets.");
    }

    const data = await response.json();

    renderResults(data);

  } catch (error) {

    resultsDiv.innerHTML = `
      <div class="ticket-card">
        <div class="error">
          ${error.message}
        </div>
      </div>
    `;

  } finally {
    loading.classList.add("hidden");
  }
});

function renderResults(results) {

  resultsDiv.innerHTML = "";

  results.forEach(ticket => {

    const priorityClass = ticket.priority.toLowerCase();

    const card = document.createElement("div");
    card.className = "ticket-card";

    card.innerHTML = `
      <div class="ticket-message">
        ${ticket.message}
      </div>

      <div class="badges">
        <span class="badge category">
          ${ticket.category}
        </span>

        <span class="badge ${priorityClass}">
          ${ticket.priority} Priority
        </span>
      </div>

      ${ticket.error ? `
        <div class="error">
          ${ticket.error}
        </div>
      ` : ""}
    `;

    resultsDiv.appendChild(card);
  });
}