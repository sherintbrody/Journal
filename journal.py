import streamlit as st
from notion_client import Client
import pandas as pd
import plotly.express as px

# Connect to Notion
notion = Client(auth=st.secrets["NOTION_TOKEN"])
database_id = st.secrets["NOTION_DB_ID"]

# Fetch journal entries
def fetch_trades():
    results = notion.databases.query(database_id=database_id)["results"]
    rows = []
    for r in results:
        p = r["properties"]
        rows.append({
            "Open Date": p["Open Date"]["date"]["start"] if p["open date"]["date"] else None,
            "Close Date": p["Close Date"]["date"]["start"] if p["close date"]["date"] else None,
            "Lot": p["Lot"]["number"],
            "Buy/Sell": p["Buy/Sell"]["select"]["name"] if p["buy/sell"]["select"] else "",
            "Instrument": p["Instrument"]["rich_text"][0]["text"]["content"] if p["instrument"]["rich_text"] else "",
            "True Seasonality": p["True Seasonality"]["select"]["name"] if p["true seasonality"]["select"] else "",
            "Entry Price": p["Entry Price"]["number"],
            "Stop Loss": p["Stop Loss"]["number"],
            "TP": p["TP"]["number"],
            "Trailing/Exit Price": p["trailing/exit price"]["number"],
            "RR": p["RR"]["number"],
            "Result": p["Result"]["number"],
            "Remarks": p["Remarks"]["rich_text"][0]["text"]["content"] if p["Remarks"]["rich_text"] else ""
        })
    return pd.DataFrame(rows)

df = fetch_trades()

# Convert dates
df["Open Date"] = pd.to_datetime(df["Open Date"])
df["Close Date"] = pd.to_datetime(df["Close Date"])

# Sidebar filters
st.sidebar.title("🔍 Trade Filters")
instrument = st.sidebar.multiselect("Instrument", df["Instrument"].unique())
direction = st.sidebar.multiselect("Buy/Sell", df["Buy/Sell"].unique())

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
if not filtered.empty:
    perf = filtered.sort_values("Close Date").copy()
    perf["Cumulative Result"] = perf["Result"].cumsum()
    fig_line = px.line(perf, x="Close Date", y="Cumulative Result", markers=True)
    st.plotly_chart(fig_line)

# Pie chart: win vs loss
st.subheader("🥧 Win/Loss Distribution")
if not filtered.empty:
    win_loss = filtered["Result"].apply(lambda x: "Win" if x > 0 else ("Loss" if x < 0 else "Break-even"))
    fig_pie = px.pie(names=win_loss, title="Trade Outcomes")
    st.plotly_chart(fig_pie)
