import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="World Dashboard", layout="wide")

# Title
st.title("🌍 World Development Dashboard")

# Load dataset
df = pd.read_excel("World_development_mesurement.xlsx")

# Clean column names
df.columns = df.columns.str.strip()

# Sidebar filter
st.sidebar.header("Filters")
country = st.sidebar.selectbox("Select Country", df["Country"].unique())

# Filter data
filtered_df = df[df["Country"] == country]

# ================= KPI SECTION =================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

try:
    col1.metric("GDP", f"{filtered_df['GDP'].values[0]:,.0f}")
except:
    col1.metric("GDP", "N/A")

try:
    col2.metric("Population", f"{filtered_df['Population Total'].values[0]:,.0f}")
except:
    col2.metric("Population", "N/A")

try:
    col3.metric("Internet Usage", f"{filtered_df['Internet Usage'].values[0]}")
except:
    col3.metric("Internet Usage", "N/A")

# ================= DATA PREVIEW =================
st.subheader(f"📄 Data for {country}")
st.dataframe(filtered_df)

# ================= CHARTS =================
col1, col2 = st.columns(2)

# GDP vs Population
with col1:
    st.subheader("📈 GDP vs Population")
    if "GDP" in df.columns and "Population Total" in df.columns:
        fig, ax = plt.subplots()
        ax.scatter(filtered_df["GDP"], filtered_df["Population Total"])
        ax.set_xlabel("GDP")
        ax.set_ylabel("Population Total")
        st.pyplot(fig)

# Life Expectancy
with col2:
    st.subheader("👨‍👩‍👧 Life Expectancy")
    if "Life Expectancy Male" in df.columns and "Life Expectancy Female" in df.columns:
        fig, ax = plt.subplots()
        ax.bar(
            ["Male", "Female"],
            [
                filtered_df["Life Expectancy Male"].values[0],
                filtered_df["Life Expectancy Female"].values[0]
            ]
        )
        st.pyplot(fig)

# ================= MORE CHARTS =================
col1, col2 = st.columns(2)

# CO2 Emissions
with col1:
    st.subheader("🌫️ CO2 Emissions")
    if "CO2 Emissions" in df.columns:
        st.bar_chart(filtered_df["CO2 Emissions"])

# Internet Usage
with col2:
    st.subheader("🌐 Internet Usage")
    if "Internet Usage" in df.columns:
        st.bar_chart(filtered_df["Internet Usage"])

# ================= TOURISM DATA CLEANING =================
# Clean currency columns if present
if "Tourism Inbound" in df.columns:
    df["Tourism Inbound"] = df["Tourism Inbound"].astype(str).str.replace('[\$,]', '', regex=True)
    df["Tourism Inbound"] = pd.to_numeric(df["Tourism Inbound"], errors='coerce')

if "Tourism Outbound" in df.columns:
    df["Tourism Outbound"] = df["Tourism Outbound"].astype(str).str.replace('[\$,]', '', regex=True)
    df["Tourism Outbound"] = pd.to_numeric(df["Tourism Outbound"], errors='coerce')

# Tourism charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("✈️ Tourism Inbound")
    if "Tourism Inbound" in df.columns:
        st.bar_chart(filtered_df["Tourism Inbound"])

with col2:
    st.subheader("🌍 Tourism Outbound")
    if "Tourism Outbound" in df.columns:
        st.bar_chart(filtered_df["Tourism Outbound"])

# ================= FOOTER =================
st.markdown("---")
st.markdown("📌 Developed using Streamlit | Data Visualization Project")