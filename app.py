import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="World Dashboard", layout="wide")

st.title("🌍 World Development Dashboard")

# Load data
df = pd.read_excel("World_development_mesurement.xlsx")
df.columns = df.columns.str.strip()

# ===== DATA CLEANING =====
def clean_column(col):
    return pd.to_numeric(df[col].astype(str).str.replace('[\$,]', '', regex=True), errors='coerce')

for col in ["GDP", "Population Total", "Tourism Inbound", "Tourism Outbound"]:
    if col in df.columns:
        df[col] = clean_column(col)

# ===== SIDEBAR =====
st.sidebar.header("Filters")

country1 = st.sidebar.selectbox("Select Country 1", df["Country"].unique())
country2 = st.sidebar.selectbox("Select Country 2 (Comparison)", df["Country"].unique())

df1 = df[df["Country"] == country1]
df2 = df[df["Country"] == country2]

# ===== KPI SECTION =====
st.subheader("📊 Key Metrics Comparison")

col1, col2, col3 = st.columns(3)

def get_value(data, col):
    try:
        return f"{data[col].values[0]:,.0f}"
    except:
        return "N/A"

col1.metric("GDP", get_value(df1, "GDP"), delta=None)
col2.metric("Population", get_value(df1, "Population Total"))
col3.metric("Internet Usage", get_value(df1, "Internet Usage"))

# ===== DATA VIEW =====
st.subheader("📄 Data Preview")
st.dataframe(df1)

# ===== COMPARISON BAR CHART =====
st.subheader("📊 Country Comparison")

metrics = ["GDP", "Population Total", "CO2 Emissions"]

metric = st.selectbox("Select Metric", metrics)

if metric in df.columns:
    values = [df1[metric].values[0], df2[metric].values[0]]

    fig, ax = plt.subplots()
    ax.bar([country1, country2], values)
    ax.set_title(metric)
    st.pyplot(fig)

# ===== INTERACTIVE CHART =====
st.subheader("📈 Scatter Analysis")

x_axis = st.selectbox("Select X-axis", df.columns)
y_axis = st.selectbox("Select Y-axis", df.columns)

fig, ax = plt.subplots()
ax.scatter(df[x_axis], df[y_axis])
ax.set_xlabel(x_axis)
ax.set_ylabel(y_axis)
st.pyplot(fig)

# ===== TOURISM =====
col1, col2 = st.columns(2)

with col1:
    st.subheader("✈️ Tourism Inbound")
    if "Tourism Inbound" in df.columns:
        st.bar_chart(df1["Tourism Inbound"])

with col2:
    st.subheader("🌍 Tourism Outbound")
    if "Tourism Outbound" in df.columns:
        st.bar_chart(df1["Tourism Outbound"])

# ===== DOWNLOAD BUTTON =====
st.subheader("⬇️ Download Data")

csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Dataset",
    data=csv,
    file_name='world_data.csv',
    mime='text/csv'
)

# ===== FOOTER =====
st.markdown("---")
st.markdown("🚀 Advanced Dashboard | Built with Streamlit")