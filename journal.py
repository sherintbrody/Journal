import streamlit as st
from streamlit_option_menu import option_menu

# --- Custom CSS for dark sidebar ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #0e1117;
        padding-top: 2rem;
    }
    [data-testid="stSidebar"] * {
        color: #cfcfcf;
        font-family: 'Segoe UI', sans-serif;
    }
    .nav-link-selected {
        background-color: #2a2a2a !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
with st.sidebar:
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=120)  # replace with your logo
    st.markdown("### Trading Journal Pro")

    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "New Trade", "Open Positions", "Trade History", "Analytics", "Settings"],
        icons=["speedometer2", "plus-circle", "briefcase", "clock-history", "bar-chart-line", "gear"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#0e1117"},
            "icon": {"color": "#cfcfcf", "font-size": "18px"},
            "nav-link": {
                "color": "#cfcfcf",
                "font-size": "16px",
                "text-align": "left",
                "margin": "5px 0",
                "--hover-color": "#262730"
            },
            "nav-link-selected": {"background-color": "#2a2a2a"},
        }
    )

    st.markdown("---")
    st.info("💡 Tip: Consistently tracking your trades is key to improvement!")

# --- Page Routing ---
if selected == "Dashboard":
    st.title("📊 Dashboard")
    st.write("Overview of performance, KPIs, and charts here.")

elif selected == "New Trade":
    st.title("📝 New Trade")
    st.write("Form to log a new trade.")

elif selected == "Open Positions":
    st.title("📂 Open Positions")
    st.write("List of currently open trades.")

elif selected == "Trade History":
    st.title("📜 Trade History")
    st.write("Table of past trades with filters.")

elif selected == "Analytics":
    st.title("📈 Analytics")
    st.write("Charts: PnL, win rate, account growth, etc.")

elif selected == "Settings":
    st.title("⚙️ Settings")
    st.write("User preferences, themes, and account settings.")
