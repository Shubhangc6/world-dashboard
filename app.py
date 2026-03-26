import streamlit as st
import pandas as pd
import plotly.express as px

# ================= PAGE CONFIG =================
st.set_page_config(page_title="World Dashboard", layout="wide")

# ================= TITLE =================
st.markdown("<h1 style='text-align: center;'>🌍 World Development Dashboard</h1>", unsafe_allow_html=True)

# ================= LOAD DATA =================
df = pd.read_excel("World_development_mesurement.xlsx")
df.columns = df.columns.str.strip()

# ================= DATA CLEANING =================
def clean_numeric(col):
    return pd.to_numeric(
        df[col].astype(str).str.replace('[\$,]', '', regex=True).str.strip(),
        errors='coerce'
    )

for col in ["GDP", "Population Total", "CO2 Emissions"]:
    if col in df.columns:
        df[col] = clean_numeric(col)

# 🔥 FINAL INTERNET USAGE FIX (CORRECT LOGIC)
if "Internet Usage" in df.columns:
    df["Internet Usage"] = df["Internet Usage"].astype(str).str.replace('%', '', regex=True).str.strip()
    df["Internet Usage"] = pd.to_numeric(df["Internet Usage"], errors='coerce')

    # If values are like 0.02 → convert to 2%
    df["Internet Usage"] = df["Internet Usage"].apply(
        lambda x: x * 100 if pd.notna(x) and x <= 1 else x
    )

# ================= SIDEBAR =================
st.sidebar.header("🔍 Filters")

country1 = st.sidebar.selectbox("Select Country", df["Country"].unique())
country2 = st.sidebar.selectbox("Compare With", df["Country"].unique())

df1 = df[df["Country"] == country1]
df2 = df[df["Country"] == country2]

# ================= FORMAT =================
def format_m(value):
    return f"{value/1_000_000:.2f} M" if pd.notna(value) else "N/A"

# ================= KPI =================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("GDP", format_m(df1["GDP"].values[0]))
col2.metric("Population", format_m(df1["Population Total"].values[0]))

internet_val = df1["Internet Usage"].values[0]
col3.metric("Internet Usage (%)", f"{internet_val:.2f}%")

# ================= COMPARISON =================
st.subheader("📊 Country Comparison")

metric = st.selectbox("Select Metric", ["GDP", "Population Total", "CO2 Emissions"])

fig_bar = px.bar(
    x=[country1, country2],
    y=[
        df1[metric].values[0],
        df2[metric].values[0]
    ],
    labels={"x": "Country", "y": metric},
    title=f"{metric} Comparison"
)

st.plotly_chart(fig_bar, use_container_width=True)

# ================= MAP =================
st.subheader("🌍 World Map")

metric_map = st.selectbox(
    "Select Metric for Map",
    ["GDP", "Population Total", "CO2 Emissions", "Internet Usage"]
)

fig_map = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color=metric_map,
    hover_name="Country",
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig_map, use_container_width=True)

# ================= TREND =================
st.subheader("📈 Trend Over Years")

if "Year" in df.columns:

    metric_trend = st.selectbox(
        "Select Trend Metric",
        ["GDP", "Population Total", "CO2 Emissions", "Internet Usage"]
    )

    trend_df = df[df["Country"].isin([country1, country2])]

    fig_line = px.line(
        trend_df,
        x="Year",
        y=metric_trend,
        color="Country",
        markers=True,
        title=f"{metric_trend} Trend Comparison"
    )

    st.plotly_chart(fig_line, use_container_width=True)

else:
    st.warning("Year column not found")

# ================= DATA =================
st.subheader("📄 Data Table")
st.dataframe(df1)

# ================= DOWNLOAD =================
csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    "⬇️ Download Data",
    csv,
    "world_data.csv",
    "text/csv"
)

# ================= FOOTER =================
st.markdown("---")
st.markdown(
    "<center>🚀 Professional Dashboard | Built with Streamlit & Plotly</center>",
    unsafe_allow_html=True
)