# 💸 AI Finance Assistant

A chat-based personal finance tracker. Tell the assistant what you spent or earned in plain English or Roman Urdu, and it logs the transaction, picks a category and updates a live analytics dashboard.

> Example: *"I spent 500 on petrol"* or *"earned 50000 salary"*

---

## 📸 Screenshots


| 

![Screenshot 1](AI%20AGENT/Ui%20Screenshots/Screenshot%202026-09-27%20214947.png)

 | 

![Screenshot 2](AI%20AGENT/Ui%20Screenshots/Screenshot%202026-09-27%20215219.png)

 | 

![Screenshot 3](AI%20AGENT/Ui%20Screenshots/Screenshot%202026-09-27%20215234.png)

 |

---

## ✨ Features

- **Natural-language logging:** chat normally and the agent infers the amount, type (income or expense) and category.
- **Bilingual:** understands and replies in English and Roman Urdu.
- **Live dashboard:** income, expense and net balance metrics, an expense split pie chart and a financial trends line chart (Plotly).
- **Summaries on request:** ask for your spending or income summary in chat.
- **Session memory:** the agent keeps context across messages within a conversation.
- **Persistent storage:** transactions are saved in a SQLite database.

---

## 🧩 Key Concepts

**Tool-calling agent.** The LLM does not write to the database itself. It decides when to call a tool (for example, to log a transaction or fetch a summary) and uses the tool's result to write its reply. The model reasons, and the tools act.

**Structured extraction from free text.** A sentence like "I spent 500 on petrol" is converted into structured data (amount, type, category) before being stored. This is what lets a chat message feed a dashboard.

**Agent orchestration with LangGraph.** LangGraph manages the agent's state and the loop between reasoning and tool use.

**Conversation memory.** LangGraph's `InMemorySaver` checkpointer keeps the chat context during a session. Transactions themselves are stored in SQLite, so financial data survives restarts even though chat memory does not.

**Multilingual prompting.** The same agent handles English and Roman Urdu input without a separate translation step.

**Data analytics with Pandas and Plotly.** Stored transactions are loaded with Pandas and turned into interactive charts for the dashboard.

---

## 🏗️ Architecture

```
User (Streamlit chat + dashboard)
        │
        ▼
  LangGraph Agent (Groq LLM via LangChain)
        │
        ├── casual / general questions → answered directly
        │
        └── log transaction / get summary
                    │
                    ▼
                 Tools
                    │
                    ▼
            SQLite database
                    │
                    ▼
   Pandas → Plotly charts in the Streamlit dashboard
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Agent orchestration | LangChain, LangGraph |
| LLM | Groq API (`ChatGroq`) |
| Frontend and dashboard | Streamlit, Plotly |
| Database and data handling | SQLite, Pandas |
| Config | python-dotenv |

---

## 📂 Project Structure

```
.
├── AI AGENT/
│   ├── Agent/
│   │   ├── agent.py        # LangGraph agent, tool definitions, Groq LLM integration
│   │   └── database.py     # SQLite initialisation and schema
│   ├── Streamlit/
│   │   └── ui.py           # Streamlit UI, dashboard and charts
│   ├── Ui Screenshots/     # Application screenshots
│   └── .env.example        # Template for environment variables
├── LICENSE
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```
git clone https://github.com/HamzaWaseem2005/Finance-Assistant-Agent.git
cd Finance-Assistant-Agent
```

### 2. Create a virtual environment

```
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```
pip install langchain langchain-core langchain-groq langgraph streamlit plotly pandas python-dotenv
```

### 4. Set environment variables

Copy `.env.example` to `.env` and add your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the app

```
streamlit run "AI AGENT/Streamlit/ui.py"
```

---

## 🔒 Notes

- API keys are loaded from environment variables via `.env`, which is excluded from version control.
- Chat memory is held in-process and resets when the app restarts. Logged transactions stay in SQLite.

---

## 🛣️ Scope & Roadmap

**Current scope**
- Single-user personal finance tracking
- Natural-language logging in English and Roman Urdu
- Dashboard with income, expenses, balance, expense split and trends

**Planned next**
- A test set of English and Roman Urdu messages to measure how accurately transactions and categories are extracted
- Edit and delete transactions through chat
- Budget limits and spending alerts
- Multi-user support with authentication
- Deployment on Streamlit Community Cloud

---

## 👤 Author

**Muhammad Hamza Waseem**
[GitHub](https://github.com/HamzaWaseem2005) · [LinkedIn](https://www.linkedin.com/in/muhammad-hamza-waseem-976535336)

## 📄 License

Apache-2.0
