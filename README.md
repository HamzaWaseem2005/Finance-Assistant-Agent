
---

```markdown
# 💸 AI Finance Assistant

AI Finance Assistant is a smart, interactive application designed to help you manage personal and business finances (expenses and incomes). By chatting in natural language (English or Roman Urdu), you can easily log transactions, check summaries, and view live analytics through a sleek dashboard.

---

## 📁 Project Structure

```text
├── AI Agent/
│   ├── agent.py         # LangGraph agent setup, tool definitions, and Groq LLM integration
│   └── database.py      # SQLite database initialization and schema setup
├── Streamlit/
│   └── ui.py            # Streamlit-based interactive web user interface and charts
├── Ui Screenshots/      # Visual screenshots of the application UI
├── .env.example         # Template for environment variables
└── requirements.txt     # Python project dependencies

```

---

## 🚀 Key Features

* **Natural Language Processing:** Simply chat with the assistant (e.g., "I spent 500 on petrol" or "earned 50000 salary"), and it will automatically infer categories and log the data.
* **Interactive Dashboard:** Real-time metrics tracking (Income, Expense, Net Balance), Expense Split (Pie Charts), and Financial Trends (Line Charts) built with Plotly.
* **Session Memory:** Uses LangGraph's `InMemorySaver` checkpointer so the agent maintains full context throughout the conversation session.
* **Bilingual Support:** Understands and responds smoothly in both English and Roman Urdu.

---

## 🧰 Technologies & Libraries Used

* **Python** (Core Programming Language)
* **LangChain & LangGraph** (Agent orchestration, state management, and tool binding)
* **Groq API / ChatGroq** (High-speed LLM integration)
* **Streamlit** (Web application and dashboard framework)
* **Plotly** (Interactive data visualization and analytics)
* **SQLite & Pandas** (Database storage and data manipulation)
* **Python-Dotenv** (Secure environment variable management)

---

## ⚙️ Installation & Setup Guide

### 1. Clone the Repository

```bash
```
git clone https://github.com/HamzaWaseem2005/Finance-Assistant-Agent.git
cd Finance-Assistant-Agent
```

```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install langchain langchain-core langchain-groq langgraph streamlit plotly pandas python-dotenv

```

### 4. Configure Environment Variables

Create a `.env` file in the root directory of your project and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here

```

### 5. Run the Application

Launch the Streamlit user interface using the following command:

```bash
streamlit run "AI AGENT/Streamlit/ui.py"

```

