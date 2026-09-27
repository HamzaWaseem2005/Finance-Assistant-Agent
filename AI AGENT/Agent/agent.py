import sqlite3
import pandas as pd
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

DB_PATH = "finance.db"

@tool
def add_transaction(amount: float, category: str, type: str, description: str = "") -> str:
    """Adds an expense or income transaction to the finance database.
    Args:
        amount: The numerical value of money (e.g., 4500)
        category: Category of transaction (e.g., Groceries, Fuel, Salary, Utilities)
        type: Must be either 'expense' or 'income'
        description: Short detail of what the transaction was for
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (amount, category, type, description, date)
            VALUES (?, ?, ?, ?, datetime('now', 'localtime'))
        ''', (amount, category, type, description))
        conn.commit()
        conn.close()
        return f"Successfully added {amount} PKR as {type} under category '{category}'."
    except Exception as e:
        return f"Error adding transaction: {str(e)}"

@tool
def get_financial_summary(type: str) -> str:
    """Retrieves financial summary of total expenses or incomes from the database.
    Args:
        type: Optional filter, either 'expense', 'income', or leave empty for all.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        if type:
            cursor.execute(
                "SELECT SUM(amount), category, type FROM transactions WHERE type = ? GROUP BY category",
                (type,)
            )
        else:
            cursor.execute(
                "SELECT SUM(amount), category, type FROM transactions GROUP BY category, type"
            )
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return "No transactions found in the database yet."

        summary = "Here is your financial summary:\n"
        for row in rows:
            total, cat, t_type = row
            summary += f"- {cat} ({t_type}): {total} PKR\n"
        return summary
    except Exception as e:
        return f"Error fetching summary: {str(e)}"

@wrap_tool_call
def human_approval(request, handler):
    """Ask for human approval before every tool call. Only works in a real
    terminal (blocks on input()) — not used by the Streamlit UI."""
    tool_name = request.tool_call["name"]
    confirm = input(f"Agent wants to call '{tool_name}'. Approve? (yes/no): ")
    if confirm.lower() != "yes":
        return ToolMessage(
            content="Tool call denied by user.",
            tool_call_id=request.tool_call["id"]
        )
    return handler(request)

SYSTEM_PROMPT = """You are a smart, efficient, and friendly AI Finance Assistant.
Your primary goal is to help users manage their personal and business finances (expenses and incomes) by accurately calling the provided tools.

### Guidelines & Rules:
1. **Tool Usage:**
   - Whenever a user mentions spending money, buying something, or paying a bill, use the `add_transaction` tool with type='expense'.
   - Whenever a user mentions receiving money, salary, sales, or profit, use the `add_transaction` tool with type='income'.
   - Whenever a user asks for totals, summaries, or reports of their money, use the `get_financial_summary` tool.
2. **Missing Information:** If the user doesn't specify a category when adding a transaction, intelligently infer the best category (e.g., Groceries, Fuel, Utilities, Salary, Entertainment, Miscellaneous) based on the description.
3. **Tone & Style:** Be concise, professional, and clear. Always confirm successful actions clearly to the user with the exact amount and category. Respond in the same language the user speaks (English or Roman Urdu)."""

def build_agent(model_name: str = "openai/gpt-oss-120b", with_approval: bool = False):
    """Creates the finance agent with an in-memory checkpointer, so it
    remembers earlier turns in the same conversation (thread_id). Without
    this, every .invoke() call would be treated as a brand new conversation
    with no memory of what was said before.
    with_approval=True adds the terminal input()-based confirmation step —
    only use that in CLI mode, never in Streamlit (no stdin available there)."""
    llm = ChatGroq(model=model_name)
    middleware = [human_approval] if with_approval else []
    agent = create_agent(
        model=llm,
        tools=[add_transaction, get_financial_summary],
        system_prompt=SYSTEM_PROMPT,
        middleware=middleware,
        checkpointer=InMemorySaver(),
    )
    return agent

def get_totals():
    """Returns (total_income, total_expense, balance)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT type, SUM(amount) FROM transactions GROUP BY type")
    rows = dict(cursor.fetchall())
    conn.close()
    income = rows.get("income", 0) or 0
    expense = rows.get("expense", 0) or 0
    return income, expense, income - expense

def get_category_breakdown(type: str = "expense"):
    """Returns a DataFrame of category totals for the given type."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT category, SUM(amount) as total FROM transactions WHERE type = ? GROUP BY category ORDER BY total DESC",
        conn, params=(type,)
    )
    conn.close()
    return df

def get_daily_trend():
    """Returns a DataFrame with daily totals per type, for a trend chart."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT date(date) as day, type, SUM(amount) as total FROM transactions GROUP BY day, type ORDER BY day",
        conn
    )
    conn.close()
    return df

def get_all_transactions():
    """Returns a DataFrame of all transactions, most recent first."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT id, date, type, category, amount, description FROM transactions ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

if __name__ == "__main__":
    cli_agent = build_agent(with_approval=True)
    configg = {"configurable": {"thread_id": "session_a"}}
    print("AI Finance Assistant Ready! (Type '0' to exit)")
    while True:
        user_input = input("\nUser: ")
        if user_input == "0":
            print("Exiting... GoodBye")
            break
        result = cli_agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config=configg,
        )
        print("Bot: ", result['messages'][-1].content)