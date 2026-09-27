import pandas as pd
from src.database import get_connection
from src.logger import get_logger

logger = get_logger("ExpenseService")

class ExpenseTrackerService:

    @staticmethod
    def add_expense(date: str, category: str, amount: float, description: str = "") -> bool:
        if amount <= 0:
            logger.warning("Attempted to add expense with invalid amount.")
            raise ValueError("Amount must be greater than 0.")

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                    (date, category, amount, description)
                )
                conn.commit()
                logger.info(f"Expense added: ${amount} for {category}")
                return True
        except Exception as e:
            logger.error(f"Error saving expense: {e}")
            raise RuntimeError("Database insertion failed.")

    @staticmethod
    def get_all_expenses() -> pd.DataFrame:
        try:
            with get_connection() as conn:
                query = "SELECT id, date, category, amount, description FROM expenses ORDER BY date DESC"
                df = pd.read_sql_query(query, conn)
                return df
        except Exception as e:
            logger.error(f"Error fetching expenses: {e}")
            return pd.DataFrame()

    @staticmethod
    def delete_expense(expense_id: int) -> bool:
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
                conn.commit()
                logger.info(f"Deleted expense ID: {expense_id}")
                return True
        except Exception as e:
            logger.error(f"Error deleting expense ID {expense_id}: {e}")
            return False