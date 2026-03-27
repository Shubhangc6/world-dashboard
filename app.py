import streamlit as st
import pandas as pd
import plotly.express as px

# ================= PAGE CONFIG =================
st.set_page_config(page_title="World Dashboard", layout="wide")

# ================= CUSTOM CSS =================
st.markdown("""
<style>
.main-title {
    text-align:center;
    font-size:40px;
    font-weight:700;
    color:#2E86C1;
}
.kpi-card {
    background-color:#F4F6F7;
    padding:15px;
    border-radius:10px;
    text-align:center;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
st.sidebar.title("🌍 Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Clustering Analysis"])

# ================= LOAD DATA =================
df = pd.read_excel("World_development_mesurement.xlsx")
df.columns = df.columns.str.strip()

# ================= CLEAN =================
def clean_numeric(col):
    return pd.to_numeric(df[col].astype(str).str.replace('[\$,]', '', regex=True), errors='coerce')

for col in ["GDP", "Population Total", "CO2 Emissions"]:
    if col in df.columns:
        df[col] = clean_numeric(col)

# ================= INTERNET FIX =================
internet_col = None
for col in df.columns:
    if "internet" in col.lower():
        internet_col = col
        break

if internet_col:
    df[internet_col] = df[internet_col].astype(str).str.replace('%', '', regex=True)
    df[internet_col] = pd.to_numeric(df[internet_col], errors='coerce')
    df[internet_col] = df[internet_col].apply(lambda x: x*100 if pd.notna(x) and x <= 1 else x)

# ================= DASHBOARD =================
if page == "Dashboard":

    st.markdown('<div class="main-title">🌍 World Development Dashboard</div>', unsafe_allow_html=True)

    # Filters
    st.sidebar.subheader("🔍 Filters")
    country1 = st.sidebar.selectbox("Select Country", df["Country"].unique())
    country2 = st.sidebar.selectbox("Compare With", df["Country"].unique())

    df1 = df[df["Country"] == country1]
    df2 = df[df["Country"] == country2]

    # KPI
    st.subheader("📊 Key Metrics")
    c1, c2, c3 = st.columns(3)

    gdp = df1["GDP"].values[0]
    pop = df1["Population Total"].values[0]
    internet = df1[internet_col].values[0] if internet_col else 0

    c1.markdown(f'<div class="kpi-card"><h3>GDP</h3><h2>{gdp/1_000_000:.2f} M</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="kpi-card"><h3>Population</h3><h2>{pop/1_000_000:.2f} M</h2></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="kpi-card"><h3>Internet Usage</h3><h2>{internet:.2f}%</h2></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Map
    st.subheader("🌍 Global Map")
    metric = st.selectbox("Select Metric", ["GDP", "Population Total", "CO2 Emissions", internet_col if internet_col else "GDP"])

    fig_map = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color=metric,
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Comparison
    st.subheader("📊 Country Comparison")

    fig = px.bar(
        x=[country1, country2],
        y=[df1[metric].values[0], df2[metric].values[0]],
        labels={"x": "Country", "y": metric}
    )
    st.plotly_chart(fig, use_container_width=True)

    # Scatter
    st.subheader("📈 Scatter Analysis")

    x_axis = st.selectbox("X-axis", df.columns)
    y_axis = st.selectbox("Y-axis", df.columns)

    fig_scatter = px.scatter(df, x=x_axis, y=y_axis)
    st.plotly_chart(fig_scatter, use_container_width=True)

# ================= CLUSTERING PAGE =================
elif page == "Clustering Analysis":

    st.markdown('<div class="main-title">🧠 Clustering Analysis</div>', unsafe_allow_html=True)

    st.info("Explore clustering insights from the integrated model")

    st.components.v1.iframe(
        "https://world-clustering-app-kjv2asyfhynuvcn6fznucz.streamlit.app/",
        height=900,
        scrolling=True
    )

# ================= FOOTER =================
st.markdown("---")
st.markdown("<center>🚀 Ultimate Dashboard | Streamlit + Plotly</center>", unsafe_allow_html=True)