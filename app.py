import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# ================= PAGE CONFIG =================
st.set_page_config(page_title="World Dashboard", layout="wide")

# ================= SIDEBAR NAVIGATION =================
st.sidebar.title("🌍 Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Clustering Analysis"])

# ================= LOAD DATA =================
df = pd.read_excel("World_development_mesurement.xlsx")
df.columns = df.columns.str.strip()

# ================= DATA CLEANING =================
def clean_numeric(col):
    return pd.to_numeric(
        df[col].astype(str).str.replace('[\$,]', '', regex=True).str.strip(),
        errors='coerce'
    )

for col in ["GDP", "Population Total", "Tourism Inbound", "Tourism Outbound", "CO2 Emissions"]:
    if col in df.columns:
        df[col] = clean_numeric(col)

# ================= INTERNET FIX =================
internet_col = None
for col in df.columns:
    if "internet" in col.lower():
        internet_col = col
        break

if internet_col:
    df[internet_col] = df[internet_col].astype(str).str.replace('%', '', regex=True).str.strip()
    df[internet_col] = pd.to_numeric(df[internet_col], errors='coerce')
    df[internet_col] = df[internet_col].apply(
        lambda x: x * 100 if pd.notna(x) and x <= 1 else x
    )

# ================= FORMAT =================
def format_m(value):
    return f"{value/1_000_000:.2f} M" if pd.notna(value) else "N/A"

# ================= DASHBOARD PAGE =================
if page == "Dashboard":

    st.markdown("<h1 style='text-align:center;'>🌍 World Development Dashboard</h1>", unsafe_allow_html=True)

    # Filters
    st.sidebar.subheader("🔍 Filters")
    country1 = st.sidebar.selectbox("Select Country", df["Country"].unique())
    country2 = st.sidebar.selectbox("Compare With", df["Country"].unique())

    df1 = df[df["Country"] == country1]
    df2 = df[df["Country"] == country2]

    # ================= KPI =================
    st.subheader("📊 Key Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("GDP", format_m(df1["GDP"].values[0]))
    col2.metric("Population", format_m(df1["Population Total"].values[0]))

    internet_val = df1[internet_col].values[0] if internet_col else 0
    col3.metric("Internet Usage (%)", f"{internet_val:.2f}%")

    # ================= MAP =================
    st.subheader("🌍 Global Map")

    metric_map = st.selectbox(
        "Select Metric",
        ["GDP", "Population Total", "CO2 Emissions", internet_col if internet_col else "GDP"]
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

    # ================= COMPARISON =================
    st.subheader("📊 Country Comparison")

    metric = st.selectbox("Select Metric for Comparison", ["GDP", "Population Total", "CO2 Emissions"])

    fig = px.bar(
        x=[country1, country2],
        y=[df1[metric].values[0], df2[metric].values[0]],
        labels={"x": "Country", "y": metric},
        title=f"{metric} Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ================= SCATTER =================
    st.subheader("📈 Scatter Analysis")

    x_axis = st.selectbox("X-axis", df.columns)
    y_axis = st.selectbox("Y-axis", df.columns)

    fig_scatter = px.scatter(df, x=x_axis, y=y_axis)
    st.plotly_chart(fig_scatter, use_container_width=True)

    # ================= MULTI COUNTRY =================
    st.subheader("🚀 Multi-Country Comparison")

    countries = st.multiselect(
        "Select Countries",
        df["Country"].unique(),
        default=[country1, country2]
    )

    if len(countries) > 1:
        multi_df = df[df["Country"].isin(countries)]

        fig_multi = px.bar(
            multi_df,
            x="Country",
            y=metric,
            color="Country"
        )

        st.plotly_chart(fig_multi, use_container_width=True)

    # ================= INSIGHTS =================
    st.subheader("🧠 Insights")

    try:
        top_gdp = df.loc[df["GDP"].idxmax()]["Country"]
        top_internet = df.loc[df[internet_col].idxmax()]["Country"] if internet_col else "N/A"

        st.success(f"🌍 Highest GDP: {top_gdp}")
        st.success(f"🌐 Highest Internet Usage: {top_internet}")
    except:
        st.warning("Insights not available")

# ================= CLUSTERING PAGE =================
elif page == "Clustering Analysis":

    st.markdown("<h1 style='text-align:center;'>🧠 World Clustering Analysis</h1>", unsafe_allow_html=True)

    st.markdown("Explore clustering-based insights below:")

    st.markdown(
        "[🔗 Open Full Clustering App](https://world-clustering-app-kjv2asyfhynuvcn6fznucz.streamlit.app/)"
    )

    st.components.v1.iframe(
        "https://world-clustering-app-kjv2asyfhynuvcn6fznucz.streamlit.app/",
        height=800,
        scrolling=True
    )

# ================= FOOTER =================
st.markdown("---")
st.markdown("<center>🚀 Premium Dashboard | Streamlit + Plotly</center>", unsafe_allow_html=True)