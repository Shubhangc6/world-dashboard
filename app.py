import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# ================= PAGE CONFIG =================
st.set_page_config(page_title="World Dashboard", layout="wide")

st.title("🌍 Advanced World Development Dashboard")

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

# 🔥 INTERNET USAGE FIX (FINAL)
if "Internet Usage" in df.columns:
    df["Internet Usage"] = df["Internet Usage"].astype(str).str.replace('%', '', regex=True)
    df["Internet Usage"] = pd.to_numeric(df["Internet Usage"], errors='coerce')

    df["Internet Usage"] = df["Internet Usage"].apply(
        lambda x: x * 100 if pd.notna(x) and x <= 1 else x
    )

# ================= SIDEBAR =================
st.sidebar.header("🔍 Filters")

countries = st.sidebar.multiselect(
    "Select Countries",
    df["Country"].unique(),
    default=df["Country"].unique()[:2]
)

metric = st.sidebar.selectbox(
    "Select Metric",
    ["GDP", "Population Total", "CO2 Emissions", "Internet Usage"]
)

# ================= KPI =================
st.subheader("📊 Key Metrics")

if len(countries) > 0:
    df_kpi = df[df["Country"] == countries[0]]

    col1, col2, col3 = st.columns(3)

    col1.metric("GDP", f"{df_kpi['GDP'].values[0]/1_000_000:.2f} M")
    col2.metric("Population", f"{df_kpi['Population Total'].values[0]/1_000_000:.2f} M")
    col3.metric("Internet Usage", f"{df_kpi['Internet Usage'].values[0]:.2f}%")

# ================= MULTI COUNTRY TREND =================
st.subheader("📊 Multi-Country Trend Comparison")

if "Year" in df.columns:

    trend_df = df[df["Country"].isin(countries)].sort_values("Year")

    fig = px.line(
        trend_df,
        x="Year",
        y=metric,
        color="Country",
        markers=True,
        title=f"{metric} Trend Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)

# ================= GROWTH RATE =================
st.subheader("📉 Growth Rate (%)")

if "Year" in df.columns and len(countries) > 0:

    growth_data = []

    for country in countries:
        temp = df[df["Country"] == country].sort_values("Year")

        if len(temp) > 1:
            first = temp[metric].iloc[0]
            last = temp[metric].iloc[-1]

            if first != 0:
                growth = ((last - first) / first) * 100
                growth_data.append((country, growth))

    growth_df = pd.DataFrame(growth_data, columns=["Country", "Growth %"])

    fig_growth = px.bar(
        growth_df,
        x="Country",
        y="Growth %",
        title=f"{metric} Growth Rate"
    )

    st.plotly_chart(fig_growth, use_container_width=True)

# ================= FORECASTING =================
st.subheader("📈 Forecast (Future Prediction)")

if "Year" in df.columns and len(countries) > 0:

    country_forecast = st.selectbox("Select Country for Forecast", countries)

    forecast_df = df[df["Country"] == country_forecast].sort_values("Year")

    if len(forecast_df) > 2:

        X = forecast_df["Year"].values.reshape(-1, 1)
        y = forecast_df[metric].values

        model = LinearRegression()
        model.fit(X, y)

        future_years = np.array(range(int(X.max()), int(X.max()) + 6)).reshape(-1, 1)
        predictions = model.predict(future_years)

        forecast_plot = px.line(
            x=list(X.flatten()) + list(future_years.flatten()),
            y=list(y) + list(predictions),
            labels={"x": "Year", "y": metric},
            title=f"{metric} Forecast for {country_forecast}"
        )

        st.plotly_chart(forecast_plot, use_container_width=True)

# ================= MAP =================
st.subheader("🌍 Global Map")

fig_map = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color=metric,
    hover_name="Country",
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig_map, use_container_width=True)

# ================= FOOTER =================
st.markdown("---")
st.markdown("🚀 Advanced Analytics Dashboard | Streamlit + Plotly + ML")