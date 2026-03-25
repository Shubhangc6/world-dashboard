import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("🌍 World Development Dashboard")

# Load dataset
df = pd.read_excel("World_development_mesurement.xlsx")

# Clean columns (important)
df.columns = df.columns.str.strip()

# Show dataset
st.subheader("📄 Dataset Preview")
st.dataframe(df)

# Sidebar filter
st.sidebar.header("Filter")

country = st.sidebar.selectbox("Select Country", df["Country"].unique())


filtered_df = df[df["Country"] == country]

# Show filtered data
st.subheader(f"📊 Data for {country}")
st.write(filtered_df)

# ----------- VISUALIZATIONS -----------

st.subheader("📈 GDP vs Population")

if "GDP" in df.columns and "Population Total" in df.columns:
    fig, ax = plt.subplots()
    ax.scatter(filtered_df["GDP"], filtered_df["Population Total"])
    ax.set_xlabel("GDP")
    ax.set_ylabel("Population Total")
    st.pyplot(fig)

# Life Expectancy
st.subheader("👨‍👩‍👧 Life Expectancy")

if "Life Expectancy Male" in df.columns and "Life Expectancy Female" in df.columns:
    fig, ax = plt.subplots()
    ax.bar(["Male", "Female"], [
        filtered_df["Life Expectancy Male"].values[0],
        filtered_df["Life Expectancy Female"].values[0]
    ])
    st.pyplot(fig)

# Internet Usage
st.subheader("🌐 Internet Usage")

if "Internet Usage" in df.columns:
    st.bar_chart(filtered_df["Internet Usage"])

# CO2 Emissions
st.subheader("🌫️ CO2 Emissions")

if "CO2 Emissions" in df.columns:
    st.bar_chart(filtered_df["CO2 Emissions"])