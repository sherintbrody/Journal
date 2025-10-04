import streamlit as st
from notion_client import Client
import pandas as pd
import plotly.express as px

# Connect to Notion
notion = Client(auth=st.secrets["NOTION_TOKEN"])
database_id = st.secrets["NOTION_DB_ID"]

# Safe field extractor
def get_field(p, key, path):
    try:
        val = p.get(key, {})
        for step in path:
            val = val[step]
        return val
    except (KeyError, IndexError, TypeError):
        return None

# Fetch journal entries
def fetch_trades():
    results = notion.databases.query(database_id=database_id)["results"]
    rows = []
    for r in results:
        p = r["properties"]
        rows.append({
            "Open Date": get_field(p, "Open Date", ["date", "start"]),
            "Close Date": get_field(p, "Close Date", ["date", "start"]),
            "Lot": get_field(p, "Lot", ["number"]),
            "Buy/Sell": get_field(p, "Buy/Sell", ["select", "name"]),
            "Instrument": get_field(p, "Instrument", ["rich_text", 0, "text", "content"]),
            "True Seasonality": get_field(p, "True Seasonality", ["select", "name"]),
            "Entry Price": get_field(p, "Entry Price", ["number"]),
            "Stop Loss": get_field(p, "Stop Loss", ["number"]),
            "TP": get_field(p, "TP", ["number"]),
            "Trailing/Exit Price": get_field(p, "Trailing/Exit Price", ["number"]),
            "RR": get_field(p, "RR", ["number"]),
            "Result": get_field(p, "Result", ["number"]),
            "Remarks": get_field(p, "Remarks", ["rich_text", 0, "text", "content"])
        })
    return pd.DataFrame(rows)

# Load and clean data
df = fetch_trades()
df["Open Date"] = pd.to_datetime(df["Open Date"], errors="coerce")
df["Close Date"] = pd.to_datetime(df["Close Date"], errors="coerce")

# Sidebar filters
st.sidebar.title("🔍 Trade Filters")
instrument = st.sidebar.multiselect("Instrument", df["Instrument"].dropna().unique())
direction = st.sidebar.multiselect("Buy/Sell", df["Buy/Sell"].dropna().unique())

filtered = df.copy()
if instrument:
    filtered = filtered[filtered["Instrument"].isin(instrument)]
if direction:
    filtered = filtered[filtered["Buy/Sell"].isin(direction)]

# Main dashboard
st.title("📊 Trading Journal Dashboard")
st.dataframe(filtered)

# Performance chart: cumulative result
st.subheader("📈 Cumulative Result Over Time")
if not filtered.empty and "Close Date" in filtered.columns:
    perf = filtered.sort_values("Close Date").copy()
    perf["Cumulative Result"] = perf["Result"].fillna(0).cumsum()
    fig_line = px.line(perf, x="Close Date", y="Cumulative Result", markers=True)
    st.plotly_chart(fig_line)

# Pie chart: win vs loss
st.subheader("🥧 Win/Loss Distribution")
if not filtered.empty:
    win_loss = filtered["Result"].fillna(0).apply(
        lambda x: "Win" if x > 0 else ("Loss" if x < 0 else "Break-even")
    )
    fig_pie = px.pie(names=win_loss, title="Trade Outcomes")
    st.plotly_chart(fig_pie)
