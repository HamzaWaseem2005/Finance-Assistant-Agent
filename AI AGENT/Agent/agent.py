import sqlite3
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

DB_PATH = "finance.db"

@tool
def add_transaction(amount: float, category: str, type: str, description: str = "") -> str:
    """Add a transaction to the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
         cursor.execute("""
            INSERT INTO transactions
            (amount, category, type, description, date)
            VALUES (?, ?, ?, ?, datetime('now', 'localtime'))
        """, (amount, category, type, description))

        conn.commit()
        conn.close()

        return f"Successfully added {amount} PKR as {type} under category '{category}'."
   except Exception as e:
        return f"Error adding transaction: {str(e)}"

@tool
def get_financial_summary(type: str) -> str:
    """Get financial totals from the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if type:
            cursor.execute(
                "SELECT SUM(amount), category, type FROM transactions "
                "WHERE type = ? GROUP BY category",
                (type,)
            )
        else:
            cursor.execute(
                "SELECT SUM(amount), category, type FROM transactions "
                "GROUP BY category, type"
            )

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return "No transactions found in the database yet."

        summary = "Here is your financial summary:\n"

        for row in rows:
            total, category, transaction_type = row
            summary += f"- {category} ({transaction_type}): {total} PKR\n"

        return summary

    except Exception as e:
        return f"Error fetching summary: {str(e)}"

@wrap_tool_call
def human_approval(request, handler):
    tool_name = request.tool_call["name"]

    confirm = input(
        f"Agent wants to call '{tool_name}'. Approve? (yes/no): "
    )

    if confirm.lower() != "yes":
        return ToolMessage(
            content="Tool call denied by user.",
            tool_call_id=request.tool_call["id"]
        )

    return handler(request)

SYSTEM_PROMPT = """You are a finance assistant.

Help the user manage income and expenses.

When the user spends money or pays for something, add it as an expense.
When the user receives money, add it as income.
Use the financial summary tool when the user asks for totals or summaries.

If the user does not give a category, choose one based on the description.

Be concise and reply in the same language as the user."""

def build_agent(model_name="openai/gpt-oss-120b", with_approval=False):
    llm = ChatGroq(model=model_name)

    middleware = [human_approval] if with_approval else []

    return create_agent(
        model=llm,
        tools=[add_transaction, get_financial_summary],
        system_prompt=SYSTEM_PROMPT,
        middleware=middleware,
        checkpointer=InMemorySaver()
    )

def get_totals():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT type, SUM(amount) FROM transactions GROUP BY type"
    )

    rows = dict(cursor.fetchall())
    conn.close()

    income = rows.get("income", 0) or 0
    expense = rows.get("expense", 0) or 0

    return income, expense, income - expense

def get_category_breakdown(type="expense"):
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        """
        SELECT category, SUM(amount) as total
        FROM transactions
        WHERE type = ?
        GROUP BY category
        ORDER BY total DESC
        """,
        conn,
        params=(type,)
    )

    conn.close()
    return df

def get_daily_trend():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        """
        SELECT date(date) as day, type, SUM(amount) as total
        FROM transactions
        GROUP BY day, type
        ORDER BY day
        """,
        conn
    )

    conn.close()
    return df

def get_all_transactions():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        """
        SELECT id, date, type, category, amount, description
        FROM transactions
        ORDER BY id DESC
        """,
        conn
    )

    conn.close()
    return df

if __name__ == "__main__":
    agent = build_agent(with_approval=True)

    config = {
        "configurable": {
            "thread_id": "session_a"
        }
    }

    print("AI Finance Assistant Ready! (Type '0' to exit)")

    while True:
        user_input = input("\nUser: ")

        if user_input == "0":
            print("Exiting... GoodBye")
            break

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            },
            config=config
        )

        print("Bot:", result["messages"][-1].content)
