import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Page config
st.set_page_config(page_title="World Dashboard", layout="wide")

# Title
st.title("🌍 Advanced World Development Dashboard")

# Load data
df = pd.read_excel("World_development_mesurement.xlsx")
df.columns = df.columns.str.strip()

# ================= DATA CLEANING =================
def clean_column(col):
    return pd.to_numeric(df[col].astype(str).str.replace('[\$,]', '', regex=True), errors='coerce')

# Clean numeric columns
for col in ["GDP", "Population Total", "Tourism Inbound", "Tourism Outbound"]:
    if col in df.columns:
        df[col] = clean_column(col)

# 🔥 FIX Internet Usage (handles %, decimal, string)
if "Internet Usage" in df.columns:
    df["Internet Usage"] = df["Internet Usage"].astype(str).str.replace('%', '', regex=True)
    df["Internet Usage"] = pd.to_numeric(df["Internet Usage"], errors='coerce')

    # Convert decimal to percentage if needed
    if df["Internet Usage"].max() <= 1:
        df["Internet Usage"] = df["Internet Usage"] * 100

# ================= SIDEBAR =================
st.sidebar.header("Filters")

country1 = st.sidebar.selectbox("Select Country 1", df["Country"].unique())
country2 = st.sidebar.selectbox("Select Country 2 (Comparison)", df["Country"].unique())

df1 = df[df["Country"] == country1]
df2 = df[df["Country"] == country2]

# ================= FORMAT FUNCTION =================
def format_millions(value):
    try:
        return f"{value/1_000_000:.2f} M"
    except:
        return "N/A"

# ================= KPI SECTION =================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

# GDP
try:
    col1.metric("GDP", format_millions(df1["GDP"].values[0]))
except:
    col1.metric("GDP", "N/A")

# Population
try:
    col2.metric("Population", format_millions(df1["Population Total"].values[0]))
except:
    col2.metric("Population", "N/A")

# Internet Usage (FIXED)
try:
    val = df1["Internet Usage"].values[0]
    if pd.notna(val):
        col3.metric("Internet Usage (%)", f"{val:.2f}%")
    else:
        col3.metric("Internet Usage", "N/A")
except:
    col3.metric("Internet Usage", "N/A")

# ================= DATA VIEW =================
st.subheader(f"📄 Data for {country1}")
st.dataframe(df1)

# ================= COMPARISON CHART =================
st.subheader("📊 Country Comparison")

metrics = ["GDP", "Population Total", "CO2 Emissions"]
metric = st.selectbox("Select Metric", metrics)

if metric in df.columns:
    try:
        values = [
            df1[metric].values[0] / 1_000_000,
            df2[metric].values[0] / 1_000_000
        ]

        fig, ax = plt.subplots()
        ax.bar([country1, country2], values)
        ax.set_title(metric)
        ax.set_ylabel("Value (Millions)")
        st.pyplot(fig)
    except:
        st.warning("Data not available for comparison")

# ================= SCATTER ANALYSIS =================
st.subheader("📈 Scatter Analysis")

x_axis = st.selectbox("Select X-axis", df.columns)
y_axis = st.selectbox("Select Y-axis", df.columns)

fig, ax = plt.subplots()
ax.scatter(df[x_axis], df[y_axis])
ax.set_xlabel(x_axis)
ax.set_ylabel(y_axis)
st.pyplot(fig)

# ================= TOURISM =================
col1, col2 = st.columns(2)

with col1:
    st.subheader("✈️ Tourism Inbound")
    if "Tourism Inbound" in df.columns:
        st.bar_chart(df1["Tourism Inbound"])

with col2:
    st.subheader("🌍 Tourism Outbound")
    if "Tourism Outbound" in df.columns:
        st.bar_chart(df1["Tourism Outbound"])

# ================= MAP VISUALIZATION =================
st.subheader("🌍 World Map Visualization")

metric_map = st.selectbox(
    "Select Metric for Map",
    ["GDP", "Population Total", "CO2 Emissions", "Internet Usage"]
)

if metric_map in df.columns:
    try:
        fig = px.choropleth(
            df,
            locations="Country",
            locationmode="country names",
            color=metric_map,
            hover_name="Country",
            color_continuous_scale="Viridis",
            title=f"{metric_map} by Country"
        )

        st.plotly_chart(fig, use_container_width=True)
    except:
        st.warning("Map could not be generated")

# ================= DOWNLOAD =================
st.subheader("⬇️ Download Data")

csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Dataset",
    data=csv,
    file_name='world_data.csv',
    mime='text/csv'
)

# ================= FOOTER =================
st.markdown("---")
st.markdown("🚀 Final Professional Dashboard | Built using Streamlit & Plotly")