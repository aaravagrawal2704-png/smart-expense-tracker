import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

# ---------- FILE SETUP ----------
FILE_NAME = "expenses.csv"

if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Date", "Month", "Category", "Amount", "Note"])
    df.to_csv(FILE_NAME, index=False)

# ---------- LOAD DATA ----------
df = pd.read_csv(FILE_NAME)

# ---------- APP UI ----------
st.set_page_config(page_title="Family Expense Tracker", page_icon="💰")
st.title("💰 Smart Monthly Expense Tracker")
st.caption("Helping parents manage money easily")

# ---------- ADD EXPENSE ----------
st.header("➕ Add New Expense")

col1, col2 = st.columns(2)

with col1:
    category = st.selectbox("Category", ["Food", "Bills", "Travel", "Medical", "Shopping", "Other"])
    amount = st.number_input("Amount (₹)", min_value=0)

with col2:
    note = st.text_input("Note (optional)")
    date = st.date_input("Date", datetime.today())

if st.button("Add Expense"):
    month = date.strftime("%B")
    new_data = {
        "Date": date,
        "Month": month,
        "Category": category,
        "Amount": amount,
        "Note": note
    }
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)
    st.success("✅ Expense Added Successfully")

# ---------- VIEW TOTAL ----------
st.header("📊 Monthly Summary")

selected_month = st.selectbox("Select Month", df["Month"].unique())

month_data = df[df["Month"] == selected_month]

total = month_data["Amount"].sum()
st.info(f"💸 Total Expense in {selected_month}: ₹{total}")

# ---------- CATEGORY SUMMARY ----------
st.subheader("📂 Category-wise Expense")
category_sum = month_data.groupby("Category")["Amount"].sum()
st.dataframe(category_sum)

# ---------- GRAPH ----------
st.subheader("📈 Expense Graph")

fig, ax = plt.subplots()
ax.bar(category_sum.index, category_sum.values)
ax.set_ylabel("Amount (₹)")
ax.set_xlabel("Category")
ax.set_title(f"Expenses for {selected_month}")

st.pyplot(fig)

# ---------- SHOW ALL DATA ----------
with st.expander("📄 View All Expenses"):
    st.dataframe(df)

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Made with ❤️ for parents | Python Project")

