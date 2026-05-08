# 🎫 AI-Powered Support Ticket Classifier

Automatically classify and prioritize customer support messages using the OpenAI API. Built with Python (FastAPI) and a live interactive demo UI.

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
```

---

## 📂 Project Structure

```
ticket-classifier-ai-agent/
├── backend/
│   ├── __init__.py
│   ├── classifier.py      # Core classification logic
│   ├── server.py          # FastAPI REST server
│   └── requirements.txt   # Python dependencies
├── sample_output.json     # Example classifier output
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
```bash
export OPENAI_API_KEY="sk-..."
```
Or create a `.env` file:
```
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
5. **Stdin support** — Pipe any JSON array directly to the CLI.

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
