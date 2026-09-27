import streamlit as st
import datetime
import plotly.express as px
from src.database import init_db
from src.services import ExpenseTrackerService
from src.logger import get_logger

logger = get_logger("StreamlitUI")

st.set_page_config(page_title="Personal Expense Tracker", page_icon="💰", layout="wide")

init_db()

st.title("💰 Personal Expense Tracker & Analytics")
st.markdown("Track your daily expenses, visualize category breakdowns, and manage your budget.")

st.sidebar.header("Add New Expense")
with st.sidebar.form("expense_form", clear_on_submit=True):
    date_val = st.date_input("Date", datetime.date.today())
    category_val = st.selectbox("Category", ["Food", "Transport", "Utilities", "Entertainment", "Shopping", "Health", "Other"])
    amount_val = st.number_input("Amount ($)", min_value=0.01, step=1.0)
    description_val = st.text_area("Description (Optional)")
    
    submitted = st.form_submit_button("Add Expense")
    
    if submitted:
        try:
            ExpenseTrackerService.add_expense(
                date=str(date_val),
                category=category_val,
                amount=amount_val,
                description=description_val
            )
            st.sidebar.success("Expense logged successfully!")
            logger.info("UI successfully registered new expense.")
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

df = ExpenseTrackerService.get_all_expenses()

if df.empty:
    st.info("No expense logs found. Use the sidebar to record your first transaction!")
else:
    col1, col2, col3 = st.columns(3)
    total_spent = df["amount"].sum()
    avg_expense = df["amount"].mean()
    total_entries = len(df)
    
    col1.metric("Total Spent", f"${total_spent:,.2f}")
    col2.metric("Average Expense", f"${avg_expense:,.2f}")
    col3.metric("Total Transactions", total_entries)
    
    st.divider()

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Expenses by Category")
        cat_df = df.groupby("category")["amount"].sum().reset_index()
        fig_pie = px.pie(cat_df, values="amount", names="category", hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_chart2:
        st.subheader("Daily Spending Trend")
        trend_df = df.groupby("date")["amount"].sum().reset_index()
        fig_line = px.line(trend_df, x="date", y="amount", markers=True, title="Spending Over Time")
        st.plotly_chart(fig_line, use_container_width=True)

    st.divider()

    st.subheader("Expense Records")
    st.dataframe(df, use_container_width=True)

    st.subheader("Manage Records")
    delete_id = st.number_input("Enter ID to Delete", min_value=1, step=1)
    if st.button("Delete Transaction"):
        if ExpenseTrackerService.delete_expense(int(delete_id)):
            st.success(f"Record {delete_id} deleted successfully.")
            st.rerun()
        else:
            st.error("Failed to delete record. Please check the ID.")