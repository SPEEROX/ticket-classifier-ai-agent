# 🎫 AI-Powered Support Ticket Classifier

Automatically classify and prioritize customer support messages using the OpenAI API.

Built with:
- Python
- FastAPI
- OpenAI GPT-4o-mini
- Optional AI-assisted frontend UI

The backend and API logic were fully developed manually.  
The frontend UI was created with AI assistance since frontend development is not my primary area of expertise.

---

## 📌 Problem Statement

Customer support teams receive high volumes of messages daily. Manual triage is slow and inconsistent. This solution uses GPT-4o-mini to instantly classify each message by **category** and **priority**, enabling automated routing and faster resolution.

---

## 🏗️ Architecture

```
Input JSON (list of messages)
        │
        ▼
  classifier.py  ◄──── OpenAI GPT-4o-mini
        │               (JSON mode, temp=0)
        ▼
  Structured JSON output
  [{ message, category, priority }]
        │
        ▼  (optional)
  FastAPI server  ─── POST /classify
        │
        ▼
 Optional Frontend UI
```

---

## 📂 Project Structure

```
ticket-classifier-ai-agent/
├── backend/
│   ├── __init__.py
│   ├── classifier.py      # Core AI classification logic
│   ├── server.py          # FastAPI REST API
│   └── requirements.txt
│
├── frontend/
│   ├── index.html         # Frontend UI
│   ├── style.css          # Styling
│   └── app.js             # API integration
│
├── sample_output.json
├── .gitignore
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/support-classifier.git
cd support-classifier
```

### 2. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Set your OpenAI API key
#### Windows PowerShell

```powershell
$env:OPENAI_API_KEY="sk-..."
```

#### Linux / macOS

```bash
export OPENAI_API_KEY="sk-..."
```

Or create a `.env` file:

```env
OPENAI_API_KEY=sk-...
```

---

## 🚀 Usage

### Option A — Run the CLI script directly

```bash
# Uses built-in sample messages
python backend/classifier.py

# Pipe in your own JSON array
echo '["My payment failed", "App is crashing", "How to reset password?"]' \
  | python backend/classifier.py
```

### Option B — Start the REST API server

```bash
uvicorn backend.server:app --reload
```

Then POST to `http://localhost:8000/classify`:

```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      "My payment got deducted but service is not activated",
      "App crashes every time I login",
      "How to change my email address?"
    ]
  }'
```

API docs available at: `http://localhost:8000/docs`

## Option C — Run with Frontend UI

Start backend server first:

```bash
uvicorn backend.server:app --reload
```

Then open:

```text
frontend/index.html
```

You can also use the VS Code Live Server extension for a better frontend experience.

The frontend connects to:

```text
http://localhost:8000/classify
```

---

## 📤 Output Format

```json
[
  {
    "message": "My payment got deducted but service is not activated",
    "category": "Billing",
    "priority": "High"
  },
  {
    "message": "App crashes every time I login",
    "category": "Technical Issue",
    "priority": "High"
  },
  {
    "message": "How to change my email address?",
    "category": "Account",
    "priority": "Low"
  }
]
```

---

## 🏷️ Categories & Priority Logic

| Category | Description |
|---|---|
| **Billing** | Payment issues, invoices, charges, subscriptions |
| **Technical Issue** | Bugs, crashes, performance problems |
| **Account** | Login, passwords, profile changes |
| **General Inquiry** | FAQs, information requests |

| Priority | When assigned |
|---|---|
| **High** | Urgent or blocking — service down, money affected |
| **Medium** | Moderate impact — degraded experience, workaround possible |
| **Low** | Informational — how-to questions, general queries |

---

## 🔧 Technical Approach

1. **OpenAI JSON Mode** — `response_format: { type: "json_object" }` forces strictly valid JSON, eliminating parsing failures.
2. **Temperature = 0** — Deterministic outputs for consistent classification.
3. **GPT-4o-mini** — Fast and cost-efficient for classification tasks.
4. **Graceful error handling** — Each message is classified independently; failures don't crash the batch.
5. **FastAPI Backend**- REST API for easy frontend and external integration.
6. **Batch Processing**- Multiple support tickets can be processed in a single request.
7. **Stdin support** — Pipe any JSON array directly to the CLI.

---

## ✅ Ways to Run the Project

This project can be used in multiple ways:

| Mode | Description |
|---|---|
| CLI Mode | Run `classifier.py` directly from terminal |
| API Mode | Use FastAPI endpoints via `/classify` |
| Frontend Mode | Use the interactive web UI connected to the backend |

This means the classifier works independently even without the frontend.

---

## 🖼️ Frontend Preview

### AI-Powered Ticket Classification UI

<img width="100%" alt="Frontend Preview" src="./assets/frontend-preview.png">

### Features

- Modern glassmorphism UI
- Real-time classification
- Responsive design
- Priority color indicators
- FastAPI backend integration
- Loading states and error handling

---

## 🧪 Sample Output

See [`sample_output.json`](./sample_output.json) for full example output with 8 messages.

---

## 📋 Requirements

- Python 3.11+
- OpenAI API key with access to `gpt-4o-mini`

---

## 📄 License

MIT

## 🤖 Note About Frontend

The backend architecture, API design, classification logic, and integration were developed manually.

Since frontend engineering is not my primary specialization, the UI layer was created with AI assistance and then integrated into the project manually.

The core AI classification pipeline, FastAPI backend, error handling, and OpenAI integration were implemented independently.

---
