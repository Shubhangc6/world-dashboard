import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# ================= PAGE CONFIG =================
st.set_page_config(page_title="World Dashboard", layout="wide")

st.title("🌍 World Development Dashboard")

# ================= LOAD DATA =================
df = pd.read_excel("World_development_mesurement.xlsx")
df.columns = df.columns.str.strip()

# ================= DATA CLEANING =================
def clean_numeric(col):
    return pd.to_numeric(
        df[col].astype(str).str.replace('[\$,]', '', regex=True).str.strip(),
        errors='coerce'
    )

for col in ["GDP", "Population Total", "Tourism Inbound", "Tourism Outbound"]:
    if col in df.columns:
        df[col] = clean_numeric(col)

# Internet Usage Fix (FINAL)
if "Internet Usage" in df.columns:
    df["Internet Usage"] = df["Internet Usage"].astype(str).str.replace('%', '', regex=True).str.strip()
    df["Internet Usage"] = pd.to_numeric(df["Internet Usage"], errors='coerce')

    # 🔥 Convert properly
    df["Internet Usage"] = df["Internet Usage"].apply(
        lambda x: x * 100 if pd.notna(x) and x <= 1 else x
    )

# ================= SIDEBAR =================
st.sidebar.header("Filters")

country1 = st.sidebar.selectbox("Select Country 1", df["Country"].unique())
country2 = st.sidebar.selectbox("Select Country 2 (Comparison)", df["Country"].unique())

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

if pd.notna(internet_val):
    col3.metric("Internet Usage (%)", f"{internet_val:.2f}%")
else:
    col3.metric("Internet Usage (%)", "0.00%")

# ================= DATA =================
st.subheader(f"📄 Data for {country1}")
st.dataframe(df1)

# ================= COMPARISON =================
st.subheader("📊 Country Comparison")

metric = st.selectbox("Select Metric", ["GDP", "Population Total", "CO2 Emissions"])

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
    st.warning("Comparison not available")

# ================= SCATTER =================
st.subheader("📈 Scatter Analysis")

x_axis = st.selectbox("X-axis", df.columns)
y_axis = st.selectbox("Y-axis", df.columns)

fig, ax = plt.subplots()
ax.scatter(df[x_axis], df[y_axis])
ax.set_xlabel(x_axis)
ax.set_ylabel(y_axis)
st.pyplot(fig)

import plotly.express as px
# =============================================================
if "Year" in df.columns:

    metric_trend = st.selectbox(
        "Select Metric for Trend",
        ["GDP", "Population Total", "CO2 Emissions", "Internet Usage"]
    )

    trend_df = df[df["Country"] == country1].sort_values("Year")

    fig = px.line(
        trend_df,
        x="Year",
        y=metric_trend,
        markers=True,
        title=f"{metric_trend} Trend for {country1}"
    )

    st.plotly_chart(fig, use_container_width=True)

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

# ================= MAP =================
st.subheader("🌍 World Map")

metric_map = st.selectbox(
    "Select Metric for Map",
    ["GDP", "Population Total", "CO2 Emissions", "Internet Usage"]
)

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

# ================= TREND OVER YEARS =================
st.subheader("📈 Trend Over Years")

if "Year" in df.columns:

    metric_trend = st.selectbox(
        "Select Metric for Trend",
        ["GDP", "Population Total", "CO2 Emissions", "Internet Usage"]
    )

    # Filter data for selected country
    trend_df = df[df["Country"] == country1]

    # Sort by year
    trend_df = trend_df.sort_values("Year")

    # Plot
    fig, ax = plt.subplots()
    ax.plot(trend_df["Year"], trend_df[metric_trend], marker='o')

    ax.set_title(f"{metric_trend} Trend for {country1}")
    ax.set_xlabel("Year")
    ax.set_ylabel(metric_trend)

    st.pyplot(fig)

else:
    st.warning("Year column not found in dataset")

# ================= INSIGHTS =================
st.subheader("🧠 Key Insights")

try:
    top_gdp = df.loc[df["GDP"].idxmax()]["Country"]
    top_internet = df.loc[df["Internet Usage"].idxmax()]["Country"]

    st.write(f"🌍 **Highest GDP Country:** {top_gdp}")
    st.write(f"🌐 **Highest Internet Usage:** {top_internet}")
except:
    st.write("Insights not available")

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
st.markdown("🚀 Professional Dashboard | Streamlit + Plotly | Portfolio Project")